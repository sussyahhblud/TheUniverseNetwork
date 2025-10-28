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
- **October 28, 2025** (Latest): Scramjet Browser Integration
  - **Browser Replacement**: Replaced the previous Scramjet-hosted browser with the full Scramjet proxy from https://github.com/sussyahhblud/scramjet
  - **Node.js Setup**: Installed Node.js 20 and pnpm package manager with all 900+ dependencies
  - **Dual-Server Architecture**: Implemented proxy system where Python server (port 5000) forwards `/browser/` requests to Node.js Scramjet server (port 3000)
  - **Workflow Addition**: Created "Scramjet Browser" workflow running `cd browser && PORT=3000 node server.js`
  - **Proxy Configuration**: Updated `server.py` to proxy Scramjet-related paths (`/browser`, `/scram/`, `/baremux/`, `/epoxy/`, `/libcurl/`, `/baremod/`, `/assets/`) to preserve proper headers
  - **Git Ignore Update**: Added Node.js patterns (node_modules, pnpm files, etc.) to `.gitignore`
  - **Fully Functional**: Scramjet browser UI loads correctly with configuration panel, though WASM placeholder limits actual proxying (as in original GitHub repo)

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
- **Browser Server (Node.js 20)**: Runs the Scramjet web proxy on port 3000 via `browser/server.js`
- **Proxy Integration**: Python server forwards `/browser/` and Scramjet-related paths to the Node.js server

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
- **Scramjet Proxy Integration:** The `/browser/` page runs the full Scramjet 2.0.0-alpha proxy with:
    - Self-hosted Node.js/Fastify server on port 3000
    - Bare server for proxy connections
    - WISP protocol support for WebSocket connections
    - Dreamland.js UI framework for the browser interface
    - Multiple transport options (baremux, epoxy, libcurl, bare-as-module)
    - Complete Scramjet codebase from sussyahhblud/scramjet repository
    - Note: Uses placeholder WASM module (0 bytes) - full proxying requires building Rust/WASM rewriter (rustup, wasm-bindgen, wasm-opt, wasm-snip)
- **Game Modifications:**
    - Cookie Clicker: Ad-free, tracking-free, and domain check bypassed for Replit iframe compatibility.
    - Crossy Road: Removed external tracking.
    - Slope: Replaced with a clean, ad-free version.
    - Minecraft/Eaglercraft: Includes a TeaVM polyfill to fix iframe runtime errors.
- **File Size Optimization:** Games are compressed by removing non-essential files (e.g., non-English localizations, source maps) and optimizing images.

**System Design Choices:**
- **Backend API:** Simple Python API for `/api/ping`, `/api/download-games`, and `/api/check-games`.
- **Proxy Architecture**: HTTP proxy from Python to Node.js using `http.client.HTTPConnection` for Scramjet paths
- **Deployment:** Configured for Replit autoscale deployment (`python3 server.py`) and compatible with Render.com Web Service deployments.
- **Error Handling:** Improved error messaging for static hosting and a dedicated deployment guide (`RENDER_DEPLOYMENT_GUIDE.md`).
- **Dependencies**: Python uses built-in stdlib only; Node.js uses 900+ packages managed by pnpm (lockfile: `browser/pnpm-lock.yaml`)

## External Dependencies
- **Dropbox:** Used as the source for game asset downloads.
- **EmulatorJS CDN:** `https://cdn.emulatorjs.org/stable/data/` for retro game emulation.
- **Scramjet Proxy:** Self-hosted from `browser/` directory (cloned from https://github.com/sussyahhblud/scramjet), runs on Node.js with 900+ npm packages.
- **Google Fonts:** Used for typography (configured in CSP headers for EmulatorJS).

## Workflows
1. **Server** (Main): `python3 server.py` on port 5000 - serves the main website and proxies browser requests
2. **Scramjet Browser**: `cd browser && PORT=3000 node server.js` on port 3000 - runs the Scramjet proxy server