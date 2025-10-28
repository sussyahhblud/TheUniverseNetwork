# The Universe Network

## Overview
The Universe Network is a static website serving as a gaming portal for multiple browser games. It features a dark-themed UI, clean navigation, and a smart download system for game assets. The project aims to provide an ad-free and distraction-free gaming experience with retro emulation and unrestricted web browsing capabilities.

## User Preferences
- I prefer simple language.
- I want iterative development.
- Ask before making major changes.
- I prefer detailed explanations.
- Do not make changes to the folder `Z`.
- Do not make changes to the file `Y`.

## Recent Updates
- **October 28, 2025** (Latest): Major UI and Game Updates
  - **UN Favicon**: Created SVG favicon with "UN" logo and added to all pages (home, games, emulator, browser, settings, and all game pages)
  - **Emulator Improvements**: Added SharedArrayBuffer detection that shows helpful deployment instructions when running in Replit's preview environment
  - **Plants vs Zombies Added**: New game using Ruffle Flash emulator, fully playable with themed navigation dropdown
  - **Super Mario World Added**: Informational page directing users to play SMW via the emulator (SNES system)
  - **CSP Updates**: Updated server.py Content Security Policy to allow Ruffle CDN resources (unpkg.com and cdn.jsdelivr.net)
  - **Game Icons**: Added PvZ and SMW icons to both the games listing page and home page modal
  - All new games integrate seamlessly with the existing theme system

## System Architecture
The application is a static website served by a Python 3.11 HTTP server (`server.py`). It uses a consistent black theme with customizable alternatives and a two-tier CSS architecture for styling.

**UI/UX Decisions:**
- **Theming System:** Five customizable themes (Classic, Midnight Blue, Charcoal, Pure White, Deep Space) persist across pages using CSS variables and JavaScript, saving preferences to `localStorage`.
- **Navigation:** Consistent top navigation for main pages (Home, Games, Emulator, Browser, Settings). In-game, a proximity-activated, themed dropdown provides navigation without cluttering the game screen.
- **Game Icons:** Uses actual images for game icons instead of emojis.
- **Download Popup:** Scrollable with enhanced logging and a UN logo.

**Technical Implementations & Features:**
- **Static File Serving:** Python's built-in HTTP server serves all static files from the current directory on `0.0.0.0:5000`.
- **Cache Control:** `Cache-Control` headers are configured to prevent caching issues.
- **Dynamic Game Download System:** Games are downloaded on-demand via a backend API (`/api/download-games`) and extracted directly into the `games/` folder. A file-system based check (`/api/check-games`) determines if games are installed.
- **EmulatorJS Integration:** The `/emulator/` page uses EmulatorJS (via CDN) for in-browser retro game emulation, supporting over 25 systems. It includes ROM file upload, save states, and gamepad support. `Cross-Origin-Embedder-Policy (COEP)` and `Cross-Origin-Opener-Policy (COOP)` headers are configured for `SharedArrayBuffer` support.
- **Scramjet Proxy Integration:** The `/browser/` page integrates Scramjet proxy for unrestricted web browsing with smart URL handling and full-screen display.
- **Game Modifications:**
    - Cookie Clicker: Ad-free, tracking-free, and domain check bypassed for Replit iframe compatibility.
    - Crossy Road: Removed external tracking.
    - Slope: Replaced with a clean, ad-free version.
    - Minecraft/Eaglercraft: Includes a TeaVM polyfill to fix iframe runtime errors.
- **File Size Optimization:** Games are compressed by removing non-essential files (e.g., non-English localizations, source maps) and optimizing images.

**System Design Choices:**
- **Backend API:** Simple Python API for `/api/ping`, `/api/download-games`, and `/api/check-games`.
- **Deployment:** Configured for Replit autoscale deployment (`python3 server.py`) and compatible with Render.com Web Service deployments.
- **Error Handling:** Improved error messaging for static hosting and a dedicated deployment guide (`RENDER_DEPLOYMENT_GUIDE.md`).

## External Dependencies
- **Dropbox:** Used as the source for game asset downloads.
- **EmulatorJS CDN:** `https://cdn.emulatorjs.org/stable/data/` for retro game emulation.
- **Scramjet Proxy:** Integrated via MercuryWorkshop's hosted service at `https://scramjet.mercurywork.shop` for web browsing functionality.
- **Google Fonts:** Used for typography (configured in CSP headers for EmulatorJS).