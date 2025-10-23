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
            'cookie-clicker',
            'crossyroad',
            'minecraft',
            'slope',
            'super-mario-64'
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
        """Download and extract UniverseGames.zip from Dropbox"""
        try:
            print("Starting game download process...")
            
            # Dropbox URL
            dropbox_url = "https://www.dropbox.com/scl/fi/iy4lpgkafq9kmqwvcvu51/UniverseGames.zip?rlkey=8o4p1r84g70igmpojk1dnttqa&st=1mx7dcga&dl=1"
            
            # Download the zip file
            print("Downloading UniverseGames.zip...")
            temp_zip = '/tmp/UniverseGames.zip'
            temp_extract = '/tmp/UniverseGames'
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            req = urllib.request.Request(dropbox_url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=120) as response:
                with open(temp_zip, 'wb') as out_file:
                    out_file.write(response.read())
            
            print("Download complete. Extracting main zip...")
            
            # Extract the main zip
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_extract)
            
            print("Main zip extracted. Processing game zips...")
            
            # Path to individual game zips
            games_dir = os.path.join(DIRECTORY, 'games')
            
            # Find the directory containing the game zips by walking the tree
            print(f"Searching for game zips in {temp_extract}...")
            source_dir = None
            
            for root, dirs, files in os.walk(temp_extract):
                # Look for directory containing .zip files
                zip_files = [f for f in files if f.endswith('.zip')]
                if zip_files:
                    print(f"Found {len(zip_files)} game zips in: {root}")
                    print(f"  Game files: {zip_files}")
                    source_dir = root
                    break
            
            if not source_dir:
                raise Exception("Could not find game zip files in downloaded archive")
            
            # Game zips to extract
            game_zips = [
                'cookie-clicker.zip',
                'crossyroad.zip',
                'minecraft.zip',
                'slope.zip',
                'super-mario-64.zip'
            ]
            
            for game_zip in game_zips:
                zip_path = os.path.join(source_dir, game_zip)
                if os.path.exists(zip_path):
                    print(f"Extracting {game_zip}...")
                    
                    game_name = game_zip.replace('.zip', '')
                    game_path = os.path.join(games_dir, game_name)
                    
                    # Remove existing folder if it exists
                    if os.path.exists(game_path):
                        shutil.rmtree(game_path)
                    
                    # Extract to temp location
                    temp_game_path = os.path.join(games_dir, f'_temp_{game_name}')
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_game_path)
                    
                    # Check if there's a nested folder
                    nested_path = os.path.join(temp_game_path, game_name)
                    if os.path.exists(nested_path):
                        shutil.move(nested_path, game_path)
                        shutil.rmtree(temp_game_path)
                    else:
                        shutil.move(temp_game_path, game_path)
                    print(f"  ✓ {game_name} extracted successfully")
                else:
                    print(f"  ✗ {game_zip} not found at {zip_path}")
            
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
