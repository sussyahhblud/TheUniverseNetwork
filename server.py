#!/usr/bin/env python3
import http.server
import socketserver
import os
import urllib.request
import json
import zipfile
import shutil
from urllib.parse import urlparse, parse_qs

PORT = 5000
DIRECTORY = "."

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        
        # Headers for webretro (enables SharedArrayBuffer)
        # Using credentialless for better compatibility with iframes
        self.send_header('Cross-Origin-Embedder-Policy', 'credentialless')
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        
        # CSP headers to allow webretro, Ruffle, service workers, and game resources
        # Whitelisted domains:
        #   cdn.jsdelivr.net - webretro cores, Ruffle emulator
        #   unpkg.com - Ruffle emulator
        #   *.googleapis.com - Firebase, Google services, imasdk for games
        #   *.firebaseio.com - Firebase realtime database for games
        #   *.google.com - Firebase auth
        #   fonts.googleapis.com/gstatic.com - Google Fonts
        csp_policy = (
            "default-src 'self' cdn.jsdelivr.net unpkg.com https://*.googleapis.com https://*.google.com; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' cdn.jsdelivr.net unpkg.com https://*.googleapis.com https://*.gstatic.com; "
            "worker-src 'self' blob: cdn.jsdelivr.net; "
            "child-src 'self' blob:; "
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net unpkg.com fonts.googleapis.com; "
            "img-src 'self' data: blob: cdn.jsdelivr.net https://*.googleapis.com; "
            "font-src 'self' data: cdn.jsdelivr.net fonts.gstatic.com; "
            "connect-src 'self' blob: data: cdn.jsdelivr.net https://*.googleapis.com https://*.firebaseio.com https://*.google.com; "
            "media-src 'self' blob: data:; "
            "object-src 'none'; "
            "frame-src 'self' blob: https://*.google.com;"
        )
        self.send_header('Content-Security-Policy', csp_policy)
        
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/api/check-games':
            self.handle_check_games()
        else:
            # Default GET handler for static files
            return super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/download-games':
            self.handle_download_games()
        elif self.path == '/api/ping':
            self.handle_ping()
        else:
            self.send_error(404, "Endpoint not found")
    
    def handle_check_games(self):
        """Check if games are installed by checking if game folders exist"""
        games_to_check = [
            '1v1lol',
            'cookie-clicker',
            'crossyroad',
            'drive-mad',
            'flappy-bird',
            'minecraft',
            'slope',
            'super-mario-64',
            '2048',
            'cuttherope',
            'cuttherope2',
            'templerun'
        ]
        
        games_dir = os.path.join(DIRECTORY, 'games')
        installed_games = []
        missing_games = []
        
        for game in games_to_check:
            game_path = os.path.join(games_dir, game)
            if os.path.exists(game_path) and os.path.isdir(game_path):
                installed_games.append(game)
            else:
                missing_games.append(game)
        
        all_installed = len(missing_games) == 0
        
        response_data = {
            'installed': all_installed,
            'installed_games': installed_games,
            'missing_games': missing_games,
            'total': len(games_to_check),
            'installed_count': len(installed_games)
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())
    
    def handle_ping(self):
        """Simple ping endpoint to check if backend is available"""
        response_data = {'status': 'ok', 'backend': 'available'}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())
    
    def handle_download_games(self):
        """Download and extract games from Dropbox folder directly to games directory"""
        try:
            print("Starting game download process...")
            
            # Dropbox folder URL - change dl=0 to dl=1 for direct download
            dropbox_url = "https://www.dropbox.com/scl/fo/1t9ufkx1n9gn3tikrt14d/AOUmORjtRogE8lMt7HDkhlY?rlkey=4vcl644pzp7yyokzc8jieklee&st=jbcb6vdr&dl=1"
            
            # Download the zip file
            print("Downloading games from Dropbox...")
            temp_zip = '/tmp/games_download.zip'
            temp_extract = '/tmp/games_extract'
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            req = urllib.request.Request(dropbox_url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=120) as response:
                with open(temp_zip, 'wb') as out_file:
                    out_file.write(response.read())
            
            print("Download complete. Extracting files...")
            
            # Extract the zip to temp directory
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_extract)
            
            print("Extraction complete. Moving files to games folder...")
            
            # Path to games directory
            games_dir = os.path.join(DIRECTORY, 'games')
            
            # Find the extracted content (Dropbox creates a folder with the share name)
            # Walk through the temp extract to find all folders and files
            extracted_items = []
            for root, dirs, files in os.walk(temp_extract):
                # Get the relative path from temp_extract
                rel_path = os.path.relpath(root, temp_extract)
                
                # Skip the root level if it's just a wrapper folder
                if rel_path == '.':
                    # Copy all immediate subdirectories and files
                    for item in dirs + files:
                        src = os.path.join(root, item)
                        extracted_items.append((item, src))
                    break
            
            # If no items at root, look one level deeper (Dropbox folder wrapper)
            if not extracted_items:
                first_level = os.listdir(temp_extract)
                if len(first_level) == 1 and os.path.isdir(os.path.join(temp_extract, first_level[0])):
                    # There's a single wrapper folder
                    wrapper_dir = os.path.join(temp_extract, first_level[0])
                    for item in os.listdir(wrapper_dir):
                        src = os.path.join(wrapper_dir, item)
                        extracted_items.append((item, src))
            
            print(f"Found {len(extracted_items)} items to move to games folder")
            
            # Copy all items directly to games folder
            for item_name, src_path in extracted_items:
                dest_path = os.path.join(games_dir, item_name)
                
                # Remove existing item if it exists
                if os.path.exists(dest_path):
                    if os.path.isdir(dest_path):
                        shutil.rmtree(dest_path)
                    else:
                        os.remove(dest_path)
                
                # Copy to games directory
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path)
                    print(f"  ✓ Copied folder: {item_name}")
                else:
                    shutil.copy2(src_path, dest_path)
                    print(f"  ✓ Copied file: {item_name}")
            
            # Clean up temp files
            print("Cleaning up temporary files...")
            if os.path.exists(temp_zip):
                os.remove(temp_zip)
            if os.path.exists(temp_extract):
                shutil.rmtree(temp_extract)
            
            print("Game download and extraction complete!")
            
            response_data = {
                'success': True,
                'message': 'All games downloaded and extracted successfully'
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            print(f"Error during game download: {str(e)}")
            error_response = {
                'success': False,
                'error': str(e)
            }
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Server running at http://0.0.0.0:{PORT}/")
        print(f"Serving directory: {os.getcwd()}")
        httpd.serve_forever()
