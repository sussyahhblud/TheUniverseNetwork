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
- **October 28, 2025** (Latest): Rammerhead Browser Integration
  - **Browser Replacement**: Replaced Scramjet proxy with Rammerhead from https://github.com/binary-person/rammerhead
  - **Node.js Setup**: Installed Node.js 20 and npm dependencies (testcafe-hammerhead based)
  - **Dual-Server Architecture**: Implemented proxy system where Python server (port 5000) forwards `/browser/` requests to Node.js Rammerhead server (port 3000)
  - **Workflow Addition**: Created "Rammerhead Browser" workflow running `cd browser && node src/server.js`
  - **Proxy Configuration**: Updated `server.py` to proxy `/browser` paths to Rammerhead, simplified from previous Scramjet implementation
  - **Configuration Override**: Created `browser/config.js` to configure Rammerhead for Replit environment (port 3000, bind to 0.0.0.0, password: sharkie4life)
  - **Fully Functional**: Rammerhead proxy interface loads with session management, URL proxying, and multi-worker support (8 workers)

- **October 28, 2025**: Replit Environment Setup
  - **GitHub Import**: Successfully imported project from GitHub to Replit
  - **Python 3.11 Installation**: Installed Python 3.11 toolchain for running the server
  - **Workflow Configuration**: Set up "Server" workflow to run `python3 server.py` on port 5000 with webview output
  - **Deployment Configuration**: Configured autoscale deployment with `python3 server.py` as the run command
  - **Git Ignore**: Created `.gitignore` file with Python, Replit, IDE, and OS-specific exclusions
  - **Verification**: Tested homepage, games page, and emulator page - all working correctly
  - Project is now fully functional in the Replit environment

- **October 28, 2025**: Major UI and Game Updates
  - **UN Favicon**: Created SVG favicon with "UN" logo and added to all pages (home, games, emulator, browser, settings, and all game pages)
  - **Emulator Improvements**: Added SharedArrayBuffer detection that shows helpful deployment instructions when running in Replit's preview environment
  - **Plants vs Zombies Added**: New game using Ruffle Flash emulator, fully playable with themed navigation dropdown
  - **Super Mario World Added**: Informational page directing users to play SMW via the emulator (SNES system)
  - **CSP Updates**: Updated server.py Content Security Policy to allow Ruffle CDN resources (unpkg.com and cdn.jsdelivr.net)
  - **Game Icons**: Added PvZ and SMW icons to both the games listing page and home page modal
  - All new games integrate seamlessly with the existing theme system

## System Architecture
The application uses a dual-server architecture:
- **Main Server (Python 3.11)**: Serves the gaming portal and static files on port 5000 via `server.py`
- **Browser Server (Node.js 20)**: Runs the Rammerhead web proxy on port 3000 via `browser/src/server.js`
- **Proxy Integration**: Python server forwards `/browser/` requests to the Node.js Rammerhead server

The frontend uses a consistent black theme with customizable alternatives and a two-tier CSS architecture for styling.

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
- **Rammerhead Proxy Integration:** The `/browser/` page runs Rammerhead v1.2.64 with:
    - Self-hosted Node.js server on port 3000 with load balancing (8 workers)
    - Testcafe-hammerhead based proxy engine
    - Session management system with localStorage and cookie syncing
    - Password protection for creating sessions (password: "sharkie4life")
    - Cross-domain port (3001) for isolated session handling
    - File-based session caching with automatic cleanup
    - Complete Rammerhead codebase from binary-person/rammerhead repository
    - Fully functional website proxying without requiring Rust/WASM compilation
- **Game Modifications:**
    - Cookie Clicker: Ad-free, tracking-free, and domain check bypassed for Replit iframe compatibility.
    - Crossy Road: Removed external tracking.
    - Slope: Replaced with a clean, ad-free version.
    - Minecraft/Eaglercraft: Includes a TeaVM polyfill to fix iframe runtime errors.
- **File Size Optimization:** Games are compressed by removing non-essential files (e.g., non-English localizations, source maps) and optimizing images.

**System Design Choices:**
- **Backend API:** Simple Python API for `/api/ping`, `/api/download-games`, and `/api/check-games`.
- **Proxy Architecture**: HTTP proxy from Python to Node.js using `http.client.HTTPConnection` for Rammerhead paths
- **Deployment:** Configured for Replit autoscale deployment (`python3 server.py`) and compatible with Render.com Web Service deployments.
- **Error Handling:** Improved error messaging for static hosting and a dedicated deployment guide (`RENDER_DEPLOYMENT_GUIDE.md`).
- **Dependencies**: Python uses built-in stdlib only; Node.js uses npm packages for Rammerhead (lockfile: `browser/package-lock.json`)

## External Dependencies
- **Dropbox:** Used as the source for game asset downloads.
- **EmulatorJS CDN:** `https://cdn.emulatorjs.org/stable/data/` for retro game emulation.
- **Rammerhead Proxy:** Self-hosted from `browser/` directory (cloned from https://github.com/binary-person/rammerhead), runs on Node.js with testcafe-hammerhead.
- **Google Fonts:** Used for typography (configured in CSP headers for EmulatorJS).

## Workflows
1. **Server** (Main): `python3 server.py` on port 5000 - serves the main website and proxies browser requests
2. **Rammerhead Browser**: `cd browser && node src/server.js` on port 3000 - runs the Rammerhead proxy server with 8 workers