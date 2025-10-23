#!/usr/bin/env python3
"""
Download Cookie Clicker images from URLs in _imglist.txt
"""
import os
import urllib.request
import time
from pathlib import Path

def download_images():
    img_folder = Path("games/cookie-clicker/img")
    imglist_file = img_folder / "_imglist.txt"
    
    if not imglist_file.exists():
        print(f"❌ Error: {imglist_file} not found!")
        return
    
    # Read all URLs from the file
    with open(imglist_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"📥 Found {len(urls)} images to download")
    print(f"📁 Downloading to: {img_folder}")
    print("-" * 60)
    
    downloaded = 0
    failed = 0
    
    for i, url in enumerate(urls, 1):
        # Extract filename from URL
        filename = url.split('/')[-1]
        filepath = img_folder / filename
        
        # Skip if file already exists
        if filepath.exists():
            print(f"⏭️  [{i}/{len(urls)}] Skipping (exists): {filename}")
            continue
        
        try:
            print(f"⬇️  [{i}/{len(urls)}] Downloading: {filename}", end=" ... ")
            
            # Download the file
            urllib.request.urlretrieve(url, filepath)
            
            # Get file size
            size_kb = filepath.stat().st_size / 1024
            print(f"✅ ({size_kb:.1f} KB)")
            
            downloaded += 1
            
            # Small delay to be polite to the server
            time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            failed += 1
            continue
    
    print("-" * 60)
    print(f"✅ Downloaded: {downloaded} images")
    if failed > 0:
        print(f"❌ Failed: {failed} images")
    print(f"📊 Total images in folder: {len(list(img_folder.glob('*')))} files")
    print("\n🎮 Cookie Clicker images are ready!")

if __name__ == "__main__":
    print("🍪 Cookie Clicker Image Downloader")
    print("=" * 60)
    download_images()
