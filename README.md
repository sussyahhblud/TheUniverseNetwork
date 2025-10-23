# 🌌 The Universe Network

A gaming portal featuring classic browser games with a sleek black and white design.

## 🎮 Featured Games

- **Cookie Clicker** - The original idle game (ad-free)
- **Slope** - Fast-paced 3D running game
- **Super Mario 64** - Classic Nintendo 64 platformer
- **Eaglercraft** - Minecraft 1.12.2 in your browser

## ✨ Features

- Clean, modern black & white design
- Proximity-activated navigation in games
- 5 customizable themes with localStorage persistence
- Mobile-responsive layout
- No ads or tracking scripts
- All games under 25MB for fast loading

## 🎨 Theme System

Choose from 5 built-in themes:
1. Classic (Default) - Pure black with white text
2. Midnight Blue - Deep blue tones
3. Charcoal - Dark gray aesthetic
4. Pure White - Inverted theme
5. Deep Space - Dark blue-black with cyan

## 🚀 Quick Start

### Local Development

```bash
python3 server.py
```

Then visit `http://localhost:5000`

### Deploy to Render

**Important**: Deploy as a **Web Service** (not Static Site) to enable the game download feature.

1. Fork this repository
2. Go to [render.com](https://render.com)
3. Create new **Web Service**
4. Connect your GitHub repo
5. Set:
   - **Build Command**: (leave empty)
   - **Start Command**: `python3 server.py`
   - **Environment**: Python 3
6. Deploy!

The app automatically detects if the Python backend is available and will display deployment instructions if backend is not found.

## 📁 Project Structure

```
├── index.html              # Homepage with game download modal
├── games/
│   ├── index.html         # Games listing page
│   ├── cookie-clicker/    # Cookie Clicker game (downloaded on-demand)
│   ├── crossyroad/        # Crossy Road (downloaded on-demand)
│   ├── slope/             # Slope game (downloaded on-demand)
│   ├── super-mario-64/    # Super Mario 64 (downloaded on-demand)
│   └── minecraft/         # Eaglercraft (downloaded on-demand)
├── settings/
│   └── index.html         # Settings page
├── icons/                 # Game icon images
├── assets/
│   └── style.css          # Global styles with theme system
└── server.py              # Python HTTP server with download API

```

## 🛠️ Technologies

- Pure HTML5, CSS3, and JavaScript
- Python HTTP server for development
- Unity WebGL (Slope)
- Eaglercraft WebSocket server
- localStorage for theme persistence

## 📜 License

Games included are open source or mirror versions:
- Cookie Clicker: [orteil.dashnet.org](http://orteil.dashnet.org/cookieclicker/)
- Slope: Clean version from Bigfoot9999/Slope-Game
- Super Mario 64: Community browser port
- Eaglercraft: Minecraft 1.12.2 web client

## 🎯 Navigation

- **Main pages**: Top navigation bar
- **In-game**: Proximity-activated dropdown (top-right corner)

---

Made with ❤️ for gamers everywhere
