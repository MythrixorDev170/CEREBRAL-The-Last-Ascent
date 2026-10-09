# Prologue Code & Pass-Test Report

**Date:** 2026-10-09  
**Branch:** prologue-addon-prototype  
**Test scope:** static/smoke validation for prologue-addon/cerebral-prologue.html

## Result summary

- **Source-level checks performed in this session:** **14/14 PASS**
- **Reproducible Node tests added to the repo:** 12
- **GitHub Actions workflow:** added at .github/workflows/prologue-smoke.yml
- **Live browser playthrough:** NOT RUN
- **Physical Android/mobile playthrough:** NOT RUN
- **30 FPS/performance measurement:** NOT RUN

The 14 source-level checks passed against the latest code inspected during this session. The latest GitHub Actions run, [37953936894](https://github.com/MythrixorDev170/CEREBRAL-The-Last-Ascent/actions/runs/37953936894), reports 12 tests passed and 0 failed. One intermediate run failed due to a stale expectation about audio attenuation; this was corrected by scoping reduced-scare attenuation to authored scare cues and updating the test. These results do not imply that the game has been completed in a browser.

## Automated checks implemented

The test file is prologue-addon/tests/prologue-smoke.test.mjs. It uses only Node's built-in test runner and checks:

1. The embedded JavaScript module passes Node syntax validation.
2. Every statically referenced $('id') exists in the HTML, with no duplicate IDs.
3. Accessibility and audio controls exist and their settings wiring is present.
4. Reduced-scare mode affects startle feedback.
5. Startup and resize both use the 1.0 mobile pixel-ratio cap.
6. The current nine-stage objective list and index clamp exist.
7. The three-step research sequence and three-node power gate exist.
8. One-shot horror cue state flags exist and random scare-roll code remains removed.
9. Wake, look, joystick, interaction, pause, and visibility handling remain present.
10. The original campaign iframe handoff remains connected.
11. Collision, robot-search, door, and waypoint logic remain represented.
12. Local storage and Web Audio setting application have guarded fallbacks.

## How to run

From the repository root, with Node.js 22 or later:

    node --test prologue-addon/tests/prologue-smoke.test.mjs

The GitHub Actions workflow runs the same command for changes on prologue-addon-prototype.

## Manual acceptance still required

- [ ] Fresh start → wake interaction → final launch, with no softlock.
- [ ] Desktop mouse-look/pointer-lock and keyboard controls.
- [ ] Mobile wake, left joystick movement, separate right-side camera drag, and all touch buttons.
- [ ] Stamina sprint/recovery and held-input release after focus loss.
- [ ] Collision at doors, corners, annex windows, and large props.
- [ ] Robot sight, sound investigation, search, target loss, and fair hiding.
- [ ] All quest gates, research order, 3-node power, items, rewards, checkpoints, and reset/retry behavior.
- [ ] Accessibility preferences persist after reload and work on the actual browser.
- [ ] Audio/caption behavior with Web Audio suspended or speech synthesis unavailable.
- [ ] Full same-origin transition into ../cerebral.html and preservation of original saves.
- [ ] Performance profiling on a representative desktop and Android phone.

## Important distinction

A PASS in the source-level section means only that the named static check passed. It is not a claim that the relevant gameplay loop has been played successfully. This report intentionally leaves browser/device checks marked NOT RUN until evidence exists.
