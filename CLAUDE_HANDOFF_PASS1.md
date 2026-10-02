# CEREBRAL: THE LAST ASCENT — PASS 1 CLAUDE HANDOFF

## Repository / branch
- Repository: MythrixorDev170/CEREBRAL-The-Last-Ascent
- Stable baseline: main
- Pass 0 baseline branch: pass-0
- Work branch for this handoff: pass-1
- Do not reset/rebase/overwrite main.

## Current development position
Pass 0 is complete and sealed. Pass 1 is the current task: Narrative Rules and Dialogue Manager.

Pass 1 goal:
1. Replace forbidden ECHO/sibling narrative wording with cyborg wording.
2. Cerebral is a planetary-scale AI and its voice is internal to the player; it must not be presented as an in-world speaker/radio/ship/station voice.
3. Remove Cerebral speaker labels from visible dialogue presentation where the locked narrative rule requires no speaker label.
4. Build ONE centralized dialogue queue/path for all dialogue.
5. Captions/subtitles must start and end with actual voice playback when voice is available.
6. Provide a length-based fallback when speech events never fire.
7. Support priority interruption correctly.
8. Cleanly recover from onend, onerror, fallback timeout, explicit interruption, scene/menu transitions, and speechSynthesis.cancel().
9. Prevent overlapping/duplicate playback.
10. Preserve gameplay, flight, HUD layout, controls, saves, mobile behavior and all Pass 0 invariants.

## Pass 0 invariants — NEVER casually change
- FLIGHT_LOCK_REGIONS = 7
- FLIGHT_LOCK_HASH = 17585cfc351ff6
- TUNE values are sealed and must remain unchanged during Pass 1.
- PAL values are sealed baseline values.
- Scripted flight test hook must remain.
- Save schema compatibility must remain.
- Pass 0 gameplay/flight behavior must remain unchanged.
- Do not change steering style, mouse steering, sensitivity, WASD mapping, camera behavior, acceleration/inertia/drag, boost or evade.
- Do not redesign the HUD.
- Do not start Pass 2 or any later pass.

## Pass 0 verification
The repository includes the original baseline curves/facts, pass0 tests/build scripts and pass0_results.json.
Pass 0 results were 56/56 tests passing with worst flight-curve difference 0 and expected flight-lock hash 17585cfc351ff6. Runtime smoke covered menu → loading → opening → play → combat with four enemies and no console issues. Visual regression was headless scene/HUD equivalence only; no GPU screenshots were available in the sandbox.

## Pass 1 locked specification
Execution plan says:
- Existing systems touched: say, voice, cerebral, opening text, log screen, scientist and unknown-ship messages.
- New system: dialogue manager with line format (text, voice source, duration, priority).
- Acceptance: no forbidden words; lines never overlap; captions hide when voice ends; without voice, captions hide after a length-based fallback.
- Automated tests: source scan for ECHO and sibling; queue ordering; priority interruption; cooldowns; fallback timer when voice never fires.
- Visual QA: captions readable on desktop and landscape mobile.
- Browser SpeechSynthesis events are unreliable; interruption/error recovery is required.

## Dialogue audit rules
### Queue
- There is one authoritative queue and one playback state.
- FIFO order must be deterministic for equal priority.
- queue.push() must not start a second speech while isPlaying is true.
- There should be one authoritative path that advances after playback completes.
- Duplicate requests should be handled intentionally; accidental double-enqueue/double-speak is a bug.
- Menu/loading/opening/gameplay transitions must clear dialogue state as appropriate and call speechSynthesis.cancel().

### Priority interruption
- Priority decides whether the new line is allowed to interrupt the current line.
- A lower-priority line must not cancel a higher-priority line.
- When interruption occurs, speechSynthesis.cancel() may not reliably fire onend, so interruption must explicitly clean current caption/timer/state and advance the queue.
- Do not silently requeue the interrupted current line unless the design explicitly requires it.

### Fallback timer
- The fallback protects dialogue playback state; it must NOT directly advance gameplay missions/objectives.
- Start the fallback early enough to cover the case where onstart never fires.
- Clear fallback on normal completion, error and interruption.
- onerror must recover the queue.
- Never allow a stale timer from an older line to terminate a newer line.
- Caption cleanup must happen on onend, onerror, fallback timeout and explicit interruption.
- Fallback duration must be bounded and deterministic enough for tests.

### Voice-disabled / unavailable behavior
- If voice is disabled or SpeechSynthesis is unavailable, dialogue must still display captions through the same manager and finish via duration fallback.
- Do not make mission progression depend on browser speech events.

## Narrative locks
- Player is a scientist-created cyborg.
- No Zyroth, fantasy village, voxel RPG, church or unrelated RPG systems.
- Cerebral is the planetary AI antagonist, not a humanoid character.
- Cerebral communication is internal/in the player's mind.
- Enemy communication becomes readable/audible only after scanning that enemy.
- Before scan, enemies can attack/lock/etc. but should not provide detailed lore comms.
- Scientist recordings are external authored recordings and are distinct from Cerebral's internal voice.
- Cerebral should be intelligent/controlled, not a generic screaming villain.
- Do not add excessive cutscenes or generic jumpscares as part of Pass 1.

## What NOT to do
- Do not weaken or delete tests merely to get green results.
- Do not invert priority semantics.
- Do not use the fallback timer to call mission progression.
- Do not create a second parallel dialogue system.
- Do not rewrite flight code.
- Do not change TUNE or PAL values.
- Do not change save behavior.
- Do not start Pass 2.
- Do not refactor unrelated gameplay systems unless strictly required for the dialogue manager.
- Do not stop after identifying a bug: implement the fix, test it, then report it.
- If a test is genuinely wrong, prove why and correct the test rather than weakening it.

## Known previous Pass 1 debugging context
A previous Claude session had already begun Pass 1 and was investigating two unexpected test failures. The reported work included:
- seal/hash check;
- escaped-newline/raw-string bug;
- event timing behavior;
- synchronous callback timing;
- token-based position matching;
- tightening an upper/exclusive-limit test.
This repository handoff is the safe GitHub baseline; inspect the actual current git diff/state before assuming any of those local edits exist on pass-1. Do not recreate work blindly.

## Required workflow
1. Inspect the repository and git status/diff first.
2. Read cerebral.html, docs/pass0/PASS0.md, docs/pass0/pass0_results.json, docs/pass0/pass0_tests.js, docs/pass0/pass0_build.py, docs/pass0/baseline_curves.json, docs/pass0/baseline_facts.json, docs/CEREBRAL_Execution_Plan.txt, docs/executive/Executive_Summary.txt, docs/design/Master_Game_Plan.txt.
3. Locate every current dialogue path: say, voice, cerebral, opening/log/scientist/unknown-ship lines.
4. Design/finish the centralized dialogue manager.
5. Implement Pass 1 only.
6. Add focused unit/state tests for FIFO ordering, no overlap, higher-priority interruption, lower-priority non-interruption, interruption cleanup when cancel does not emit onend, onerror recovery, onstart never firing, fallback expiry, stale timer isolation, voice-disabled fallback, transition cleanup, duplicate prevention, forbidden ECHO/sibling scan, and no Cerebral speaker label in visible dialogue markup/text.
7. Run the complete Pass 0 regression suite as well as the new Pass 1 tests.
8. Re-run flight-lock verification. Expected hash remains 17585cfc351ff6.
9. Run syntax/build checks.
10. Run headless runtime smoke if available.
11. Do not declare Pass 1 complete until tests and regression checks are actually run.
12. Commit the finished Pass 1 implementation and tests to this branch.
13. Do not begin Pass 2.

## Final report required
Report files changed; exact dialogue architecture; tests added/changed; full test result; Pass 0 result; flight-lock hash/result; forbidden-word scan result; runtime smoke result; known limitations/visual QA still requiring browser/GPU; and commit SHA.