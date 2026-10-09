# CEREBRAL: THE LAST ASCENT — Horror Prologue Add-on

This branch contains an expanded first-person prologue prototype that hands off to the existing spacecraft campaign. It remains isolated from the protected game source.

## Run it locally

From the repository root, start a static server:

```bash
python -m http.server 8000
```

Open `http://localhost:8000/prologue-addon/cerebral-prologue.html`. The page imports Three.js from jsDelivr, so an internet connection is required.

**Use a same-origin static server for the launch handoff.** At the end of the prologue, the page loads the repository's existing `../cerebral.html` into a full-screen frame. If no campaign save exists, it selects New Game and begins the original game's first mission. If saves exist, it leaves the original campaign menu open so the player can choose Continue, Load, or New Game without silently overwriting a save.

## Prologue flow now in code

1. Wake and manually release Hibernation Unit 07 in a larger, high-ceiling hibernation chamber.
2. Recover the neural stabilizer and medical access chip.
3. Enter the central deck and explore the connected vessel wings.
4. Restore facility power by routing **three separate nodes** across Maintenance and Research.
5. Recover the research archive, then the crew recording in Communications.
6. Reach Security, override the hangar lockdown, release the ship and enter the cockpit.
7. Watch the short in-engine launch transition, then continue into the existing CEREBRAL campaign.

Three optional memory fragments provide extra story context without blocking the main route. Cerebral remains a voice/caption only; this build contains no visible Cerebral character, model, or face.

## Current systems

- Enlarged room proportions, tall chamber ribs and trusses, deterministic stars/debris placement, procedural panel/floor textures, hangar cradle dressing, wrecked utility robots and environmental clues.
- Keyboard/mouse first-person movement with acceleration/deceleration, sprint and crouch; touch joystick, drag-look, interact, decoy, breath, crouch and sprint controls on coarse-pointer devices.
- Structural room/corridor/door collision, door collision while shut, interaction line-of-sight checks, milestone checkpoints and local recovery after a capture.
- Robot vision-cone checks, structural occlusion, shorter detection range while crouched, sound investigation, last-known-position search, pursuit and fair hidden-state loss. The robots are still a lightweight prototype AI, not a full navigation-mesh implementation.
- Heart-rate, breathing, noise and neural-stability HUD; controlled breathing while hidden; thrown metal decoys and loud power routing to draw a search toward the last sound location.
- Authored one-shot central-deck and Communications cues. Random scare rolls have been removed; remaining procedural geometry placement is deterministic.
- Three relay interactions, security/recording gating, optional memory pickups and a ship-launch handoff into the actual campaign HTML.

## Important limits

This is still a procedural vertical-slice implementation, not the finished 12–18-minute jam release. Models, surfaces, decals and audio are mostly generated placeholders; the current audio is synthesized tones/ambience rather than recorded, spatially occluded voice and sound assets. Collision covers structural geometry and selected large props rather than every small prop. Robot navigation is deliberately simple, and the full run time, difficulty curve and route have not been measured in a browser playthrough.

The prototype's JavaScript module body passes a syntax compilation check and its static DOM references resolve, but browser runtime, the full end-to-end quest, iframe handoff, mobile touch behavior, real-device performance and audio still need hands-on testing. Do not call the prototype fully tested until those checks have actually been run.

## Protected source boundary

`cerebral.html` is intentionally unchanged on this branch and has the same blob SHA as `pass-1`. The prologue's launch handoff opens that original file rather than duplicating or rewriting its ship, flight physics, save schema, HUD, targeting, weapons or campaign state.

Claude's integration task is to continue from this implementation—not to recreate it from scratch—then test the full prologue and existing regression suites before merging any isolated prelude hook. Do not change the protected `pass-1` branch.
