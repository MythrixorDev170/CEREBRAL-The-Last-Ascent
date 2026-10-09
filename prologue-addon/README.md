# CEREBRAL: THE LAST ASCENT — Horror Prologue Add-on

This branch contains a larger first-person horror prelude that hands off to the original spacecraft campaign. Recent work adds collision-backed crew-habitat and observation-gallery wings, a Unit 07 interior/hatch wake-up beat, 6.4m annex ceilings, 7.2m primary-bay/deck/hangar ceilings, and upper structural gantries. The protected `pass-1` branch and the authoritative `cerebral.html` have not been modified.

## Run

From the repository root:

```bash
python -m http.server 8000
```

Open `http://localhost:8000/prologue-addon/cerebral-prologue.html`. Three.js is imported from jsDelivr, so an internet connection is required.

Run through a **same-origin static server** for the campaign handoff. After the in-engine launch, the prelude loads the repository's original `../cerebral.html` in a full-screen frame. When no campaign save exists, it chooses New Game and starts the original first mission. When saves exist, it leaves the original game's menu available and asks the player to choose Continue/Load/New Game. Existing save data is not overwritten by the prelude.

## Implemented route

1. Tap Begin Recovery; Unit 07's hatch releases automatically, so the player is never stuck waiting for a wake prompt.
2. Use the neural stabilizer and recover the medical access chip.
3. Enter the central space deck and move through the ship's opened bulkheads.
4. Restore the grid by activating **three separate power nodes** in Maintenance and Research. The loud grid restore can attract a nearby security robot.
5. Complete the Research containment sequence in order: **ISOLATE → VERIFY → PURGE**, then access the encrypted archive.
6. Recover the crew recording in Communications, then use the Security override.
7. Release the hangar lockdown.
8. Reconnect the spacecraft cradle's power coupler.
9. Enter the cockpit, watch the short in-engine launch, and transition into the original CEREBRAL campaign.

Five optional memory fragments add story context. Cerebral has no visible character/model/face; lines are spoken with browser speech synthesis when available and are also shown as subtitles. This is a fallback implementation, not final recorded voice acting.

## Systems in the prototype

- Animated 3D title camera; extended multi-zone vessel layout with connected crew-habitat and panoramic observation-gallery wings; stacked bunks, lockers, survey consoles, a first-person Unit 07 viewport and animated release hatch, 7.2m hibernation/central/hangar spaces, 6.4m annexes, tall structural ribs and ceiling gantries, bulkhead frames, distant planet/moon, procedural panel/floor textures, a batched starfield, deterministic debris, crew traces, broken utility frames, dust and restrained steam sprites.
- Smooth first-person movement with acceleration/deceleration, normal walking, a faster walk toggle (`V` / FAST WALK touch button), stamina-limited sprint with delayed recovery, crouch, non-accumulating head bob/lean and FOV response, camera-height control, player/wall/door collision, contextual line-of-sight interactions and an objective waypoint with bearing and distance.
- Touch joystick plus a dedicated right-side drag-look zone (independent from movement), Interact/Hide, fast-walk toggle, decoy, breath control, crouch, stamina-limited sprint and pause controls on coarse-pointer devices. Begin Recovery releases the pod automatically; look drag no longer competes with joystick input. Touch controls use pointer capture and reset sprint/crouch/breath state on release/cancel.
- Muted industrial-horror HUD (less neon/cyberpunk styling), heart rate/breath/noise/neural-stability and stamina meters, controlled breathing while hidden, a short proximity heartbeat effect, vignette-based stress feedback (no full-frame CSS blur on mobile) and recoverable checkpoints.
- Three procedural security robots: two patrol/hunt units and a heavy central-deck frame that remains dark until facility power is restored. Behavior includes forward-cone vision, darker-area/crouch visibility reductions, structural occlusion, footstep/power/decoy sound investigation, navigation through a simple authored waypoint graph, last-known-position searches, coordinated alerting and a short pursuit state. Robots can lose the player; this is not a full navmesh or behavior-tree AI implementation.
- Thrown metal decoys, a mandatory three-step lab terminal puzzle, room-specific footstep tones, panned/occluded synthetic threat tones, emergency red strobes, grid-linked fading room lights and scripted one-shot environmental cues.
- Automatic launch handoff to the original game HTML. No flight mechanics, weapons, targeting, HUD, mission logic or save format have been copied or modified in this prelude.

## Known limits

This is still a **procedural vertical slice**, not the finished 12–18-minute jam release. Room surfaces, most props, robot models and environmental stains are primitive/generated assets. Audio is browser TTS plus synthesized ambience/tones, not recorded actors or a fully spatial/occluded sound library. Collision covers architectural walls, bulkheads, the annex windows and selected large objects, not every small piece of dressing. Robot navigation is a small waypoint graph and can still make imperfect search decisions. The duration has not yet been measured from a real playthrough.

Mobile performance settings reduce pixel ratio, disable antialiasing and real-time shadow maps on coarse-pointer devices, cache repeated box/cylinder geometry, reuse collision raycast lists, and avoid full-frame CSS blur; desktop retains the higher pixel-ratio cap and shadows. **The latest edits have passed a JavaScript syntax check, but have not yet been verified in a live browser or on a physical phone.** Touch look, sprint stamina, quest completion, collision edge cases, speech synthesis, iframe handoff, mobile/Safari behavior and actual frame rate still need hands-on testing. Do not treat a static parse as a game-play test.

## Protected source boundary

`cerebral.html` is byte-for-byte unchanged on this branch compared with `pass-1`. The prologue is deliberately an add-on that loads the original campaign rather than replacing it. Continue from this implementation—do not recreate it from scratch—and test the whole route before merging an integration hook. Never edit the protected `pass-1` branch directly.
