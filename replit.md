# The Universe Network - Replit Setup

## Overview
The Universe Network is a gaming portal featuring multiple browser games. It's a static website with a black theme, clean navigation, and a smart download system for game assets.

## Recent Updates
- **October 23, 2025**: All game files have been extracted from UniverseGames.zip (downloaded from Dropbox) and are now fully integrated into the games folder. All games are now available and functional.

## Project Structure
- `index.html` - Homepage with UN logo
- `games/index.html` - Games listing page
- `settings/index.html` - Settings page
- `assets/style.css` - Shared stylesheet for Universe Network theme
- `server.py` - Simple Python HTTP server for serving static files
- `games/cookie-clicker/` - Cookie Clicker game
  - `index.html` - Main game page
  - `main.js` - Core game logic
  - `style.css` - Game styling
  - `img/` - Game images and sprites
  - `snd/` - Game sound effects
  - `loc/` - Localization files

## Setup
This project uses Python 3.11's built-in HTTP server to serve static files on port 5000 with cache control headers disabled to ensure updates are visible.

## Development
The workflow runs `python3 server.py` which:
- Serves all static files from the current directory
- Binds to 0.0.0.0:5000 for Replit compatibility
- Includes cache-control headers to prevent caching issues

## Deployment
Configured for autoscale deployment using the same Python HTTP server.

## Features
- Clean black-themed navigation across all pages
- Homepage with bold "UN" logo and "The Universe Network" title
- Games page with clickable game cards
- Smart download system for Cookie Clicker assets
- Settings page (placeholder for future expansion)

## Available Games
- **Cookie Clicker** - The original idle game (ad-free) at `/games/cookie-clicker/`
- **Crossy Road** - Classic road-crossing arcade game at `/games/crossyroad/`
- **Super Mario 64** - Classic Nintendo 64 platformer at `/games/super-mario-64/`
- **Slope** - Fast-paced 3D running game at `/games/slope/`
- **Minecraft/Eaglercraft** - Minecraft 1.12.2 in your browser at `/games/minecraft/Web/`

## Navigation

### Main Pages (Home, Games, Settings)
All main pages include a consistent navigation bar at the top:
- **UN Logo** (top-left) - Clickable logo that returns to homepage
- **Navigation buttons** (top-right):
  - **Home** - Main landing page
  - **Games** - Browse available games
  - **Settings** - Configuration options

### In-Game Navigation
When playing games (like Cookie Clicker), the top bar is removed for a clean gaming experience. Instead, a small white dropdown button appears in the top right corner when your mouse gets close to that area (proximity-activated). Clicking it reveals a dropdown menu featuring:
- The UN logo (styled like the homepage)
- "The Universe Network" title
- Navigation links to Home, Games, and Settings

The button automatically fades in when your mouse moves near the top-right corner and fades out when you move away, keeping the game screen completely clean until you need navigation.

## Cookie Clicker
- Original game: http://orteil.dashnet.org/cookieclicker/
- GitHub mirror: https://github.com/ozh/cookieclicker
- Accessible at `/games/cookie-clicker/`
- Save games stored in localStorage
- **All ads removed** (Google AdSense, Facebook Pixel, cookie consent, etc.)
- Clean gaming experience with no tracking or advertisements
- **Smart Download System**: Click the Cookie Clicker card to show a popup that downloads all 310+ PNG images from the original source on-demand
  - Theme-aware popup modal matching the website aesthetic
  - Progress tracking with detailed error reporting
  - Automatic redirect to game after successful download
  - Backend API endpoint at `/api/download-images`

## Crossy Road
- Source: https://github.com/tw31122007/HTML-Games-V2
- Accessible at `/games/crossyroad/`
- Classic arcade-style road-crossing game with 3D graphics
- Removed external tracking scripts for clean gameplay

## Modifications for Replit
The original game includes a domain check that prevents it from running in iframes (which Replit uses for previews). This check has been bypassed by commenting out the iframe detection code in `main.js` at line 16868:
```javascript
// Commented out: if (top!=self) Game.ErrorFrame();
```
This allows the game to run properly in the Replit environment while maintaining all original functionality.

## File Size Optimization
All games have been compressed to stay under 25MB:

### Cookie Clicker (9MB - down from 14MB)
- Removed non-English localization files (kept English only)
- Optimized PNG images with optipng
- Optimized JPEG images with jpegoptim (max quality 85%)
- Removed global stylesheet to prevent UI conflicts

### Slope (9.7MB - clean version)
- Replaced with clean version from Bigfoot9999/Slope-Game (GitHub)
- Removed all ads, tracking scripts, and rick roll content
- Clean Unity WebGL build without bloat
- Integrated with Universe Network navigation system

### Minecraft/Eaglercraft (20MB - down from 22MB)
- Removed source map file (classes.js.map) which isn't needed for production

## Theme System
The site includes 5 customizable themes saved to localStorage:
1. **Classic** (Default) - Pure black background with white text
2. **Midnight Blue** - Deep blue tones with light blue text
3. **Charcoal** - Dark gray background with light gray text
4. **Pure White** - Inverted theme with white background and black text
5. **Deep Space** - Dark blue-black with cyan blue highlights

Themes persist across all pages (Home, Games, Settings) using CSS variables and JavaScript.
