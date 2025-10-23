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
    
    def do_POST(self):
        if self.path == '/api/download-games':
            self.handle_download_games()
        elif self.path == '/api/ping':
            self.handle_ping()
        else:
            self.send_error(404, "Endpoint not found")
    
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
            dropbox_url = "https://www.dropbox.com/scl/fi/zqa64ofwfwy1tz0111vbo/UniverseGames.zip?rlkey=ro2wm7h08gnmhqkhtkp4n173s&st=tl46gfqy&dl=1"
            
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
            source_dir = os.path.join(temp_extract, 'UniverseGames/games/games')
            
            # Game zips to extract
            game_zips = [
                'index.zip',
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
                    
                    if game_zip == 'index.zip':
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            zip_ref.extractall(games_dir)
                    else:
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
