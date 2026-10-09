# CEREBRAL: THE LAST ASCENT — First-Person Horror Prologue Add-on

## What this is
A standalone, single-file Three.js playable prototype intended as a concrete starting point for Claude to improve and integrate. It is **not** the production game's merged build and does not modify the existing `cerebral.html` or any protected game systems.

## Play
Open `cerebral-prologue.html` in a browser with internet access. It imports Three.js from jsDelivr. If your browser blocks ES modules on `file://`, serve this folder with a local static server (for example, `python -m http.server 8000`) and open `http://localhost:8000/prologue-addon/cerebral-prologue.html`.

Controls: WASD move, mouse look, E interact/hide/leave hiding, Shift sprint, Ctrl crouch, Q control breathing while hidden, Esc pause/release mouse. Click Resume to reacquire the mouse.

## Prototype currently contains
- First-person mouse-look movement, sprint/crouch, pause/restart, HUD/objective updates.
- A connected, authored station layout with Medical Bay, Central Space Deck and planet view, Maintenance, Research, Security, Communications and Hangar.
- Modular industrial room geometry, medical pods, benches, consoles, crates, pipework, windows, warning accents, broken/sparking panel, starfield and planet.
- Recoverable stabilizer, access chip, power relay, research archive, security override, crew recording, hangar release and cockpit interactions.
- Heart-rate, breathing-control, noise and neural-stability feedback.
- Two procedural facility robots with basic patrol/investigate/pursuit/search behavior; proximity threat and one authored scare beat.
- Cerebral objective reactions, scientist recording, generated ambience/tones, hangar/cockpit launch ending.
- Responsive UI and capped renderer pixel ratio.

## Important prototype limits — Claude must address before claiming production-ready
This is a playable greybox/vertical-slice foundation, not the final 12–18-minute jam-ready experience. Geometry is procedural, art/audio are placeholders, the stealth simulation is intentionally simple, and full physical collision/navigation, polished room connections, enemy animation, proper objective gating, accessibility settings, real recorded voice assets, browser/device testing and performance soak still need implementation and verification. The ending contains an explicit integration handoff rather than actually loading the current game's first state. Do not describe it as merged or fully tested.

## Claude's task: improve this implementation, do not remake it
Read this file first, then the current authoritative CEREBRAL source/build and Pass 8–12 reports. Work from this prototype as the starting point. Preserve its useful scene structure and interactions, then integrate the prologue as an isolated opening module into the **actual current game**. Do not replace the whole game with this prototype.

Non-negotiable preservation: keep the existing player ship and all current ship geometry/materials, flight physics and flight-lock protected regions/hash, TUNE, PAL, spacecraft controls, damage, weapons, targeting, hitboxes/collision, Pass 8 adaptation/comms, Pass 9–11 world/visual/hangar systems, Pass 12 horror director/audio architecture, existing mission progression, and save schema unchanged except for the smallest isolated prologue-completion flag if truly required. Do not rebalance spacecraft combat or change existing enemy stats.

Priority order:
1. Make the first-person prologue truly playable end-to-end: reliable collision and traversable doorways; clear navigation; no softlocks; robust objective gating; interact ray/line-of-sight; checkpoint/recovery; real robot search logic based on vision, sound, light and last-known location; hiding spaces with fair detection; controlled-breath timing that affects audible detection; predictable authored scare budget; no random unfair deaths.
2. Upgrade environment quality with detailed, consistent material variation, readable silhouettes, motivated lighting, restrained volumetric-looking steam/dust, authored sparks, decals, props and strong spatial composition. Avoid excessive fog, constant flicker and indiscriminate darkness. Keep it performant.
3. Make audio cues directional and distinct; reuse the existing audio architecture and Pass 12 director. Add recorded voice assets only when available; gracefully handle missing assets.
4. Build a rewarding 12–18-minute route: wake/recover, explore, investigate, first hunt, breathing hide, research revelation, second coordinated hunt, hangar escape, launch. Optional data/recordings should reveal story or grant useful prologue intel, not grind.
5. Replace the placeholder ending with a deterministic handoff into the **exact current game's first-area/start state**. Use the existing ship, existing world and existing game state; do not create a second ship or duplicate campaign. If exact handoff cannot be proven, stop and report the precise missing integration point rather than guessing.
6. Test desktop Chromium, a narrow/mobile-emulated viewport, keyboard/mouse and available touch fallback; run existing Pass 1–12 regression suites and flight-lock checks. Report exact pass/fail counts and any untested physical-device/browser limitations. Never claim tests were run if they were not.

Design direction: original industrial sci-fi psychological survival horror, taking only high-level lessons from excellent horror games (tension, sensory AI, environmental storytelling, systemic risk/reward, coordinated searches). Do not copy their characters, level layouts, audio, dialogue or distinctive mechanics. Cerebral is a planet-scale AI/network, not a humanoid monster. It reacts selectively to objective milestones with a calm-to-manipulative-to-threatening arc (examples: “You're awake.”, “Nice try.”, “You unlocked it.”, “Hide.”). Avoid constant chatter and repetitive jumpscares.

Finish with the actual updated game build plus a concise change report, test evidence, known limits, and a rollback-safe diff. Keep the implementation focused; no unrelated features or new pass framework.
