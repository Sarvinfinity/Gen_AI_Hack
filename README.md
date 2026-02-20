# AgroGenesis AI — Digital Twin Simulator (Enhanced)

This workspace contains `agrogenesis-enhanced.html`, an interactive 3D digital twin simulator for field terrain, crops, weeds, and an autonomous robot.

## Features
- 3D terrain and crop surface (Plotly surface)
- Weed clusters with pest contagion dynamics
- Weed-aware A* navigation: path cost increases for weed-dense cells
- Robot auto-play animation along A* path
- Spray action to clear weeds along the route
- Hotspot mode: click 3D cells to toggle weeds
- Analytics: growth curve, weed forecast, EcoScore, environmental impact
- 2D heatmap with robot path overlay
- EcoScore canvas ring showing combined score (temp, rain, yield, weeds)
- Events: Pest Outbreak (spreads weeds), Drought Scenario (reduces yield)
- Compare mode: CURRENT vs DAY 1 snapshots
- Layer toggles for weeds, crops, path, heatmap, robot
- Animated loading screen and UI controls

## Quick Start
You can open the HTML directly or serve it with a simple local HTTP server (recommended).

Option A — Open directly
- Double-click `agrogenesis-enhanced.html` or open it in your browser.
- Note: some browsers restrict local file features; using a local server avoids this.

Option B — Python 3 HTTP server (recommended)
Open PowerShell in this folder and run:

```powershell
# start simple server on port 8000
python -m http.server 8000
# then open file in default browser (Windows)
Start-Process "http://localhost:8000/agrogenesis-enhanced.html"
```

Option C — Node (http-server)
```powershell
# install once if needed
npm i -g http-server
# serve current directory
http-server -p 8000
# open in browser
Start-Process "http://localhost:8000/agrogenesis-enhanced.html"
```

## Controls / Tips
- Left sidebar: adjust day, environment, robot start/goal
- Overlays: toggle weeds, path, crops, heatmap, robot
- `AUTO PLAY` animates days and robot traversal
- `SPRAY PATH` removes weeds along the current path
- `HOTSPOT MODE`: click on the 3D view to toggle weed presence
- `SIMULATE PEST EVENT` toggles increased spread behavior
- `DROUGHT SCENARIO` reduces crop growth by ~60%
- Use the `ANALYTICS` and `FIELD HEATMAP` tabs for charts and 2D view

## Where to edit
- `agrogenesis-enhanced.html` contains all code (single-file app)
- Look for sections labeled: TERRAIN, WEEDS, A*, RENDERING, ANALYTICS

## Next steps (suggested)
- Add persistent save/load for `dayHistory` snapshots (localStorage)
- Integrate real sensor feeds or GeoTIFF terrain
- Add multiple robot agents and scheduling

If you want, I can also start a local preview server now or add a quick `run.bat` to automate launching the browser.