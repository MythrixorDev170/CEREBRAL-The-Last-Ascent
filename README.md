# CEREBRAL: THE LAST ASCENT

3D sci-fi horror/action game prototype for the October game jam theme **“AI is going to kill us!”**

## Current source

- **`cerebral.html`** — complete current playable game source.
- Uses **Three.js r128** from cdnjs at runtime.
- Current build is intentionally a single-file browser game; no build step is required.

## Run

Open `cerebral.html` in a modern browser with internet access.

## Current systems

- Third-person spacecraft flight
- Mouse steering inside a bounded central steering zone
- Touch/mobile controls
- Boost and evade movement
- Primary laser and homing missile combat
- Enemy classes: Drone, Soldier, Elite and Warden
- Target lock, shield/hull HUD and weak-point scanning
- Shield-generator combat loop and hull damage
- Hacking system
- Cerebral internal dialogue/transmissions
- Scientist/research narrative elements
- Horror/anomaly events and ghost-ship encounter foundation
- Research, military/industrial, refuge, wreck and safe-point regions
- Missions, survivor extraction and delivery
- Credits, parts, data and upgrade progression
- Safe-point repair/upgrade flow
- Autosave and safe-point local saves
- Main menu, loading transition, opening sequence
- Tutorial
- Control remapping
- Audio/display/gameplay settings
- Procedural Web Audio effects
- Desktop and mobile presentation

## Important baseline

This repository is the **current source baseline** for continued development and game-jam iteration. The game is still under active development; planned improvements include higher-fidelity authored 3D assets, deeper environments/interiors, expanded missions and horror sequences, stronger map/checkpoint progression, dialogue/voice synchronization, combat feedback, materials/lighting polish, optimization and additional QA.

## Source provenance

The current `cerebral.html` was uploaded from the project's complete source-code document and represents the current playable baseline.

## Pass 0 (safety net)

See `pass0/PASS0.md`. Results: `pass0_results.json`. Open `cerebral.html?perf=1` for the debug overlay.