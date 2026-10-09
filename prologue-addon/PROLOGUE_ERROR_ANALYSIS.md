# CEREBRAL: The Last Ascent — Prologue Error Analysis

**Review date:** 2026-10-09  
**Review branch:** prologue-addon-prototype  
**Scope:** The standalone first-person prologue in prologue-addon/cerebral-prologue.html, using the uploaded Prologue Design Report as the intended specification.  
**Safety boundary:** pass-1 is protected and was not used as a write target. The original cerebral.html campaign is still loaded through the prologue handoff rather than replaced.

## Executive assessment

The latest prototype already has a more developed route than the uploaded report's five-quest outline: it contains nine objective stages, a three-node facility power gate, a three-step Research containment sequence, memory fragments, hiding/decoys, robot search behavior, and a hangar/cockpit handoff. The report and code are therefore **not yet content-equivalent**. This pass preserved the prototype's current progression instead of replacing it with a second incompatible quest system.

This pass adds player-comfort options and reproducible smoke tests. Source-level checks passed in the working session, but that is not a substitute for playing through the complete game in a browser or on a phone.

## Findings by priority

| Priority | Finding | Evidence / likely impact | Status |
|---|---|---|---|
| P0 | End-to-end browser and physical-device verification is still required. | Static parsing cannot confirm first-person feel, touch behavior, door/collision edge cases, robot fairness, voice playback, or final campaign iframe handoff. | **Open — manual acceptance required.** |
| P0 | The report's exact puzzle/quest list is not the implementation currently in the repository. | Report lists pod code 2187, Blue → Green → Red lab keypad, wire-matching elevator panel, and a maintenance drone beat. Current code instead has a nine-stage route, three independent power nodes, and ISOLATE → VERIFY → PURGE. | **Open — design reconciliation required.** |
| P1 | Target playtime has not been measured. | The report targets roughly 18–20 minutes. The README describes a procedural vertical slice and explicitly says a full-route duration has not been measured. | **Open — timed playtest required.** |
| P1 | Audio is procedural/browser-generated, not the final sound package. | The prototype synthesizes tones and ambience through Web Audio and uses browser speech synthesis for Cerebral. It does not yet provide recorded actor dialogue and a full licensed industrial-horror library. | **Open — production audio pass.** |
| P1 | Enemy navigation is a lightweight waypoint graph, not a full navigation system. | Current README documents authored waypoint navigation and imperfect search decisions. Some collision coverage is architectural walls and selected large props rather than all dressing. | **Open — test patrol routes and corners.** |
| P1 | The generic scare helper appears to be uncalled. | Source inspection found the helper definition, while intended scares are driven by the authored wreck, blackout, communications, and robot-trigger blocks. An unused helper can mislead future tuning. | **Open — remove it or deliberately wire it to one authored event after playtesting.** |
| P1 | The report's specified jumpscares are only partially represented. | Existing code has one-shot wreck-motion cues, a blackout/observation cue, a communications cue, and a robot investigation trigger. It does not yet guarantee the exact corridor-door slam, vent drone, and hangar lunge scenes in the report. | **Open — stage and test only after route validation.** |
| P2 | The prototype remains a large single HTML/module file with stacked CSS overrides. | Fast to prototype, but it makes features harder to isolate and regressions harder to localize. | **Deferred — refactor after the jam route is stable.** |
| P2 | Real performance and memory behavior are unmeasured. | The mobile pixel-ratio cap is now consistent at 1.0 during startup and resize, and touch devices disable real-time shadow maps; neither guarantees 30 FPS on every phone. | **Open — profile representative devices.** |
| P2 | Keyboard focus and screen-reader behavior need a browser review. | The settings dialog returns focus to its opener and exposes dialog semantics, but a full focus trap, screen-reader pass, and visual zoom test have not been performed. | **Partially improved; review required.** |

## Changes made in this pass

1. Added an Accessibility & Audio panel reachable from both the intro screen and pause menu.
2. Added a persisted Reduce jumpscare effects option. It reduces low-frequency startle tones and wreck twitch intensity, and removes the helper's red screen flash in reduced mode.
3. Added configurable dialogue captions, Cerebral speech synthesis, Audio Comfort, and a 0–100 master volume.
4. Wrapped local-storage reads/writes and optional Web Audio use in guards so settings do not crash when those browser APIs are unavailable.
5. Added dialog focus handoff and focus return.
6. Standardized the mobile renderer pixel-ratio cap at 1.0 for initial setup and resize.
7. Added a Node.js smoke-test suite and a GitHub Actions workflow on the prototype branch.

## Verification performed in this session

**Source consistency checks: 13/13 passed.** The checks used the latest branch source and a JavaScript parser in this tool session. They covered inline-module syntax, test-file syntax, all $('id') references having a matching unique DOM ID, the nine-stage objective array, mobile pixel ratio, accessibility controls, reduced-scare wiring, the three-node power gate, authored scare flags, touch wake/visibility safety, original-campaign handoff, and collision/robot/door/waypoint function presence.

The repository Node test file contains 12 reproducible tests. A source-level check is not a completed run of node --test, and the GitHub Actions result must be checked before describing those tests as CI-passed. No live browser or physical-phone session was run in this pass.

## Recommended remediation order

### P0 — Before calling the prologue complete
- Run node --test prologue-addon/tests/prologue-smoke.test.mjs and confirm the GitHub Actions run succeeds.
- Play from a fresh launch to the final handoff on desktop Chrome.
- Repeat on a representative Android phone, including wake, look-drag, joystick isolation, held inputs, focus loss, pause/resume, and reload.
- Validate every mandatory item, gate, checkpoint, failed puzzle retry, and robot pursuit from start to finish.
- Decide whether the current nine-stage route supersedes the report's five quests, or whether the three named legacy puzzles are mandatory additions. Do not combine them without a designed dependency graph.

### P1 — Horror, AI, and pacing
- Time at least three blind playthroughs; record slow, average, and fast completion times.
- Check whether the existing scare cues register without repeating too often. Then author the missing corridor/vent/hangar moments only where they fit the tested route.
- Ensure a robot detects by plausible vision, sound, light, or last-known position; verify that a quiet player can break pursuit.
- Replace placeholder tones and speech synthesis with appropriately licensed recorded ambience/SFX and final dialogue when production assets are available.
- Confirm the reduced-scare mode meaningfully softens authored scares without removing required clues.

### P2 — Polish
- Profile frame time and memory on target devices; inspect scene construction and repeated-geometry disposal.
- Consolidate duplicate CSS rules after visuals are approved.
- Split the monolithic script only after the current play route is stable enough for regression testing.
- Run keyboard-only, captions, volume, zoom, and screen-reader checks.

## Acceptance standard

Do not claim complete merely because the source parses. Completion requires a green automated smoke-test run, a successful desktop full-route walkthrough, a successful mobile controls walkthrough, and verified progression from the pod to the original spacecraft game without modifying the protected campaign branch.
