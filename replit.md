# The Universe Network

## Overview
The Universe Network is a gaming portal featuring multiple browser games with a dark-themed UI, clean navigation, and a smart download system for game assets. The project provides an ad-free and distraction-free gaming experience with retro emulation capabilities.

## User Preferences
- I prefer simple language.
- I want iterative development.
- Ask before making major changes.
- I prefer detailed explanations.
- Do not make changes to the folder `Z`.
- Do not make changes to the file `Y`.

## Recent Updates
- **October 29, 2025** (Latest): Emulator Replacement - Migrated from EmulatorJS to webretro
  - **webretro Integration**: Completely replaced EmulatorJS with webretro (RetroArch ported to WebAssembly)
  - **19+ Emulator Cores**: webretro v6.5 provides support for NES, SNES, Genesis, GBA, N64, PlayStation, and 14+ other systems
  - **Pre-compiled & CDN-based**: All cores load from cdn.jsdelivr.net (no build process required)
  - **Full Feature Set**: ROM upload, save states, SRAM saves, gamepad support, screenshot manager, cheats, and shaders
  - **CSP Improvements**: Updated Content Security Policy from blanket wildcards to domain-scoped allowlists (cdn.jsdelivr.net, Firebase/Google domains for games, Ruffle CDN)
  - **COEP/COOP Headers**: Cross-Origin-Embedder-Policy and Cross-Origin-Opener-Policy correctly configured for SharedArrayBuffer support
  - **Verified Working**: Tested with N64 (mupen64plus_next) core - games loading successfully without errors or black screens
  - **Documentation**: Added CSP comments documenting required domains for webretro, Firebase-enabled games, and Ruffle

- **October 29, 2025**: GitHub Import to Fresh Replit Environment
  - **Fresh Setup**: Successfully imported project from GitHub to a new Replit environment
  - **Python 3.11 Installation**: Installed Python 3.11 toolchain for running the server
  - **Workflow Configuration**: Set up "Server" workflow to run `python3 server.py` on port 5000 with webview output
  - **Deployment Configuration**: Configured autoscale deployment with `python3 server.py` as the run command
  - **Git Ignore**: Created `.gitignore` file with Python, Replit, IDE, and OS-specific exclusions
  - **Verification**: All pages (home, games, emulator, settings) and API endpoints verified working
  - Project is fully functional and ready to use in the Replit environment

- **October 29, 2025** (Replaced): EmulatorJS Integration with Replit Preview Support [REPLACED BY WEBRETRO]
  - **Service Worker Integration**: Implemented COI (Cross-Origin Isolation) service worker to enable SharedArrayBuffer in Replit's preview iframe environment
  - **EmulatorJS CDN Integration**: Configured to use official EmulatorJS CDN for optimal performance and compatibility
  - **EmulatorJS v4.0+**: Using latest stable version with full WebAssembly support for 25+ gaming systems
  - **Replit Preview Compatible**: Emulator now works in Replit's preview environment without requiring full deployment (auto-reloads once on first visit)
  - **Architecture**: Service worker injects COEP/COOP headers at runtime, enabling SharedArrayBuffer support in iframe contexts
  - **Local Reference Files**: Downloaded EmulatorJS library files (1.1MB) stored in `/emulator/emulatorjs/` for reference
  - **CSP Optimized**: Content Security Policy configured to never block EmulatorJS, service workers, or game resources
  - **Full Functionality**: Emulator supports 25+ systems with ROM upload, save states, and gamepad support
  
- **October 29, 2025**: Browser/Rammerhead Removal and CSP Fix
  - **Browser Feature Removed**: Completely removed all browser proxy/Rammerhead functionality from the application
  - **Server Cleanup**: Removed proxy code, browser endpoints, and http.client imports from server.py
  - **CSP Headers Fixed**: Relaxed Content Security Policy to allow all necessary resources (EmulatorJS, Ruffle, game assets) without blocking
  - **Navigation Updated**: Removed browser links from Plants vs Zombies dropdown menu to match site-wide navigation
  - **Single Server Architecture**: Now running on Python-only server (no Node.js dependency)
  - **Simplified Deployment**: Project ready for deployment with just `python3 server.py`

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
The application uses a simple single-server architecture:
- **Main Server (Python 3.11)**: Serves the gaming portal and static files on port 5000 via `server.py`
- **No External Dependencies**: Uses only Python standard library (http.server, socketserver, urllib, json, zipfile, shutil)

The frontend uses a consistent black theme with customizable alternatives and a two-tier CSS architecture for styling.

**UI/UX Decisions:**
- **Theming System:** Five customizable themes (Classic, Midnight Blue, Charcoal, Pure White, Deep Space) persist across pages using CSS variables and JavaScript, saving preferences to `localStorage`.
- **Navigation:** Consistent top navigation for main pages (Home, Games, Emulator, Settings). In-game, a proximity-activated, themed dropdown provides navigation without cluttering the game screen.
- **Game Icons:** Uses actual images for game icons instead of emojis.
- **Download Popup:** Scrollable with enhanced logging and a UN logo.

**Technical Implementations & Features:**
- **Static File Serving:** Python's built-in HTTP server serves all static files from the current directory on `0.0.0.0:5000`.
- **Cache Control:** `Cache-Control` headers are configured to prevent caching issues.
- **Dynamic Game Download System:** Games are downloaded on-demand via a backend API (`/api/download-games`) and extracted directly into the `games/` folder. A file-system based check (`/api/check-games`) determines if games are installed.
- **webretro Integration:** The `/emulator/` page uses webretro v6.5 (RetroArch ported to WebAssembly) for in-browser retro game emulation, supporting 19+ systems including NES, SNES, Genesis, GBA, N64, and PlayStation. Cores are loaded from `cdn.jsdelivr.net`. Includes ROM file upload, save states, SRAM saves, gamepad support, screenshot manager, cheats, and shaders. `Cross-Origin-Embedder-Policy (COEP)` and `Cross-Origin-Opener-Policy (COOP)` headers are configured for `SharedArrayBuffer` support.
- **Ruffle Flash Emulator:** Plants vs Zombies uses Ruffle Flash emulator with canvas rendering fallback for broad compatibility.
- **Improved CSP Headers:** Content Security Policy configured with domain-scoped allowlists (cdn.jsdelivr.net for webretro/Ruffle, Firebase/Google domains for game services, Google Fonts) to balance security with functionality.
- **Game Modifications:**
    - Cookie Clicker: Ad-free, tracking-free, and domain check bypassed for Replit iframe compatibility.
    - Crossy Road: Removed external tracking.
    - Slope: Replaced with a clean, ad-free version.
    - Minecraft/Eaglercraft: Includes a TeaVM polyfill to fix iframe runtime errors.
    - Plants vs Zombies: Dropdown navigation menu matches site-wide navigation (no browser link).
- **File Size Optimization:** Games are compressed by removing non-essential files (e.g., non-English localizations, source maps) and optimizing images.

**System Design Choices:**
- **Backend API:** Simple Python API for `/api/ping`, `/api/download-games`, and `/api/check-games`.
- **Deployment:** Configured for Replit autoscale deployment (`python3 server.py`) and compatible with Render.com Web Service deployments.
- **Error Handling:** Improved error messaging for static hosting and a dedicated deployment guide (`RENDER_DEPLOYMENT_GUIDE.md`).
- **Dependencies**: Python uses built-in stdlib only - no external packages required!

## External Dependencies
- **Dropbox:** Used as the source for game asset downloads.
- **webretro CDN:** `https://cdn.jsdelivr.net/gh/BinBashBanana/webretro/` for retro game emulation cores and assets.
- **Ruffle CDN:** `https://unpkg.com/@ruffle-rs/ruffle` for Flash game emulation.
- **Firebase/Google Services:** Used by some games (e.g., 1v1lol) for authentication, database, and analytics.
- **Google Fonts:** Used for typography (configured in CSP headers).

## Workflows
1. **Server**: `python3 server.py` on port 5000 - serves the entire application