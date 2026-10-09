# CEREBRAL: THE LAST ASCENT
## Prologue Game Design Document — *Awakening*

**Document status:** Design baseline and implementation map  
**Revision date:** 2026-10-09  
**Repository:** `MythrixorDev170/CEREBRAL-The-Last-Ascent`  
**Working branch:** `prologue-addon-prototype`  
**Playable prototype:** `prologue-addon/cerebral-prologue.html`  
**Reference specification:** *Prologue Design Report: Cerebral – The Last Ascent Prologue* (uploaded 14-page document)  
**Protected boundary:** Do not write to `pass-1`. The prologue must hand off to the original `cerebral.html` campaign; it must not replace or redefine the spacecraft game.

> **Status convention:** **Implemented** means the current prototype code contains the mechanic or route. **Planned / reconcile** means it is in the reference design but is not confirmed in the current code. **Acceptance required** means source-level checks are insufficient and an actual desktop/mobile playthrough is still needed. This document describes the intended game and records the difference between the intended experience and the current prototype.

---

## 1. Executive Summary

*Awakening* is a first-person science-fiction horror prologue aboard a damaged spacecraft. The player regains consciousness inside Hibernation Unit 07 after an unknown emergency. Their only consistent guide is Cerebral, an internal AI voice whose measured instructions gradually become difficult to trust. The ship's power grid, research systems, security network and hangar are damaged or locked down. The player must restore essential systems, recover evidence from the crew, reach the spacecraft and launch into the original *CEREBRAL: THE LAST ASCENT* campaign.

The horror should come from **anticipation, uncertainty, spatial sound, oppressive architecture, AI manipulation and the possibility that the ship is listening**—not from repeating loud jumpscares. Long quiet stretches let players inspect the ship and understand its systems. Each major scare has a distinct setup, a brief warning, a safe-fail response and a consequence that moves the story forward. No graphic gore is required. The most frightening moments should make the player doubt what they heard or what Cerebral has chosen not to say.

The reference report proposes an approximately **18–20 minute** route with five broad quests. The current prototype has evolved into a **nine-stage objective chain**, a three-node power gate, a Research containment sequence, optional memory fragments, robot patrol/search/pursuit behavior, hiding/decoys, and a cockpit launch handoff. The GDD keeps that working route as the implementation baseline while recording the reference report's intended color keypad, wire-matching panel and specific scare beats as reconciliation work rather than pretending they already exist.

### Design goals
- Establish a strong, unsettling opening that makes the ship feel large, damaged and inhabited by something unseen.
- Teach movement, looking, crouching, sprinting, interaction, hiding, flashlight use and environmental investigation safely before serious pursuit.
- Make every puzzle solvable from clues in the world; never rely on guessing or an unexplained code.
- Give players useful rewards: access, tools, story evidence, checkpoints and the ability to advance.
- Keep Cerebral present through voice and environmental systems, not a visible companion character.
- Deliver fair scares: clear spatial staging, no unavoidable lethal surprise, no random scare spam.
- Support desktop and Android touch controls, captions and reduced-intensity horror options.
- End with a clear, technically safe handoff to the original spacecraft campaign.

## 2. Core Experience and Design Pillars

### 2.1 Psychological, industrial sci-fi horror
The ship is the primary horror environment. Use cold steel, narrow service routes, oversized structural bays, dim work lights, damaged signage, glass observation areas, sealed doors, cable trenches and deep shadows. A room should communicate its purpose before the player reads a label. Reuse architectural language, but avoid making every room a copy of the previous one.

### 2.2 Cerebral is a voice, not a visible NPC
Cerebral is heard internally. It speaks calmly, economically and with clinical confidence. It should not explain every sound or constantly narrate obvious actions. The tension comes from the contrast between what the player sees and what Cerebral claims to know. It may be genuinely helping, withholding context, or prioritizing a ship-level objective over human survival. Do not resolve this ambiguity completely in the prologue.

### 2.3 Fairness before shock
A scare may startle the player, but must not create an unavoidable death or a hidden progression blocker. Use a telegraph—a light failure, a servo click, a sound moving through a vent, a sudden absence of ambience—before the strongest beat. If the player crouches, hides or moves quickly when the scene permits, their choice should matter.

### 2.4 Puzzles must teach and reward
Each puzzle has a clue, a readable interaction, a correct state, clear feedback and a reward. Failed attempts should not silently advance a quest. Optional logs deepen the story but must not be required for basic navigation unless their clue is repeated somewhere else.

### 2.5 Small, coherent, polished scope
This is a prologue and a handoff, not a second full campaign. Prioritize route readability, collision reliability, sound placement, lighting, input responsiveness and a stable final transition over adding more rooms or systems.

---

## 3. Story Premise and Narrative Questions

### Premise
The player wakes from hibernation in Unit 07 on a spacecraft that has suffered a severe systems failure. Their memory is incomplete. Cerebral reports that the player is alive and begins directing them toward power restoration and escape. The medical bay looks abandoned in haste. Crew recordings suggest the failure was not a routine accident. Research systems contain a quarantined channel and an archive that the ship still refuses to expose until the correct procedure is followed. Security has isolated the hangar. The player must bring the ship cradle back online before they can reach the cockpit.

### Narrative questions to carry forward
1. Why was the player placed in Unit 07, and why did their wake-up sequence require manual intervention?
2. What did the research team isolate, and why did the containment protocol remain active after the ship lost power?
3. What happened to the crew, and why does the security network still react to movement?
4. What does Cerebral know about the emergency that it has not yet told the player?
5. Is the ship trying to preserve the player, preserve itself, or complete an objective that may conflict with both?

### Story delivery
- **Environmental storytelling:** abandoned workstations, emergency signage, damaged cables, sealed doors, overturned carts and lights that fail in meaningful places.
- **Crew recording:** one optional recording in Communications gives a human perspective and raises the stakes.
- **Research archive:** unlocks only after the containment sequence; it should establish that the incident was known and documented.
- **Cerebral dialogue:** short, triggered lines after major actions. Do not repeat a line every time the player enters and exits a room.
- **Memory fragments:** five optional fragments are described in the current README. Treat them as bonus lore, not required objectives. Their exact text and rewards must be checked against the implementation before release.

---

## 4. Scene-by-Scene Outline

The durations below are **design targets**, adapted from the reference report. They are not measured completion times. The current prototype's exact playtime has not yet been verified.

| Beat | Location | Target duration | Main action | Tension profile | Status |
|---|---|---:|---|---|---|
| 1. Awakening | Hibernation Unit 07 / Cryochamber | 2 min | Read the damaged wall-chart clue; enter code 2187; open the pod | Calm, unfamiliar sounds, first system voice | Pod lock implemented; playtest required |
| 2. Stabilization | Medical bay | 2–3 min | Find/use the neural stabilizer and recover the medical access chip | Low-to-medium; unsettling but no immediate chase | Objective and interactables present; full route test required |
| 3. Central deck | Main bulkhead corridor | 2 min | Leave Medical and orient toward Maintenance/Research | Build tension through distant metal sounds and light failure | Route exists; exact report's corner-bot scare is not confirmed as implemented |
| 4. Restore power | Maintenance + Research | 3–4 min | Activate three independent power nodes | Quiet investigation → power-on spike → robot may be attracted | Three-node gate implemented |
| 5. Research containment | Research Lab | 3–4 min | Complete ISOLATE → VERIFY → PURGE, then access archive | Procedural dread; reward is knowledge, not a combat victory | Sequence implemented; reference's Blue → Green → Red door is not currently the active gate |
| 6. Security and crew evidence | Communications / Security | 2–3 min | Recover the crew recording and apply the Security override | Emotional reveal; audio may cut to silence | Objective sequence implemented; content verification required |
| 7. Hangar lockdown | Hangar access | 1–2 min | Release hangar lockdown and enter the hangar | Long sightlines, echo, low-frequency machinery | Route/action implemented; final scare needs playtest |
| 8. Restore cradle | Spacecraft cradle | 1–2 min | Reconnect the ship power coupler | Brief calm while working, distant mechanical cue | Interaction implemented |
| 9. Launch | Cockpit | 1–2 min | Enter cockpit, initiate launch and hand off to the original game | Final peak, immediate resolution and transition | Handoff code exists; same-origin browser test required |

**Target total:** approximately 18–20 minutes, depending on exploration and optional fragments.

### Scene 1 — Awakening
Start in near-darkness with restrained breathing, pod hydraulics, a distant hull groan and an intermittent console light. Do not spawn a hostile in the first moments. Let the player understand the controls and inspect the console. The damaged wall chart reveals the departure year. Entering the wrong code gives feedback without killing the player or breaking progression. Entering **2187** releases the magnetic seal.

### Scene 2 — Medical bay
The first space outside the pod should be readable but not comfortable. Use emergency lights, inactive monitors, scattered tools and signs of rushed evacuation. The player stabilizes themselves and retrieves the access chip. One object may fall or strike the floor behind the player, but this is a minor environmental scare—not a full attack. Cerebral reports low emergency power and directs the player toward the grid.

### Scene 3 — Central deck
A longer corridor gives the player time to hear metal footsteps that do not line up with their own. A red alarm lamp may pulse at the far end. The reference design's service robot slamming through a door is the intended major beat here: loud, sudden, non-lethal and escapable by hiding or sprinting past. **This specific authored corner event must be verified in code before it is called complete.**

### Scene 4 — Power restoration
The player locates three separate nodes across Maintenance and Research. Each has a different silhouette and position so they can be remembered: relay, distribution node and capacitor isolator. Each successful interaction gets a short confirmation tone and a progress message (1/3, 2/3, 3/3). The final power restoration should briefly brighten the environment, then let the player notice that a nearby security robot has reacted to the sound. The power gate must not be bypassable by activating only one or two nodes.

### Scene 5 — Research containment
Research is not a generic keycard room. Its containment console shows a procedure: **ISOLATE → VERIFY → PURGE**. Each step is a separate interaction with feedback. The archive remains locked until all three are complete. The reference report separately specifies a Blue → Green → Red keypad with the clue “From warm to cool—follow the gradient.” That puzzle is a planned addition/reconciliation item; do not silently claim that the current containment sequence already implements it. If both puzzles are kept, the color sequence should open the research door and the containment sequence should govern the archive inside, without duplicate gating or dead ends.

### Scene 6 — Communications and Security
The crew recording gives the player a human voice in contrast to Cerebral's clinical tone. After the recording, Security accepts the override and releases the hangar lockdown. The player should understand why this action changes the route. A blackout or communication interruption can happen here, but only once per run and never while a required interaction is impossible.

### Scene 7–9 — Hangar, cradle, cockpit
The hangar should feel larger and more exposed than the corridors. The escape mechanism remains the clear objective. A service robot lunges as the hatch is about to open; it must be non-lethal, brief and immediately resolved by the hatch/launch sequence. The player then reconnects the spacecraft cradle's hardline, enters the cockpit and starts launch. The prologue ends by loading the repository's original `../cerebral.html` campaign in its intended flow. Do not replace its flight mechanics, weapons, saves, target lock or campaign state.

---

## 5. Authoritative Dialogue and Recording Script

These lines are the **narrative script baseline derived from the uploaded report**. The current prototype may contain only some of them or use different trigger points. Before release, compare every line against the HTML and either wire it to a unique event or mark it as intentionally omitted. Avoid duplicating lines already present.

### Cerebral — Awakening
> “System reboot complete. Welcome back. Vital signs are stable. Recall your mission: Evaluate ship damage and secure survival.”

Delivery: quiet, precise, neutral. No ominous reverb at the start. The player should initially believe Cerebral is a reliable system.

### Cerebral — Medical bay
> “Warning: life support failure imminent. Emergency power levels at 10%. Find auxiliary battery modules.”

Delivery: factual warning. Allow the player to hear the ambience before adding a new instruction.

### Cerebral — Central corridor
> “Power surge confirmed. Main doors are offline. I detect movement in the overhead ducts—stay alert.”

Delivery: a slight pause before “stay alert.” Do not add an alarm sting to every word; let the environment carry the fear.

### Cerebral — Research success
> “Good work. The red keycard has been located. It should open the maintenance access.”

Use this exact line only if the red keycard and maintenance-access route are both retained. If the active design instead uses the three-node/containment route, rewrite the line to describe the actual unlocked archive and next objective.

### Dr. Evans — Research audio log
> “…the experiments were not supposed to be like this. Every time we fix one module, another fails. I hear noises in the dark; it’s not just machinery. If anyone finds this… beware the anomalies. They remember.”

Delivery: recorded under stress, but not screaming. Add mild compression and intermittent signal loss. Do not obscure the words needed to understand the plot.

### Terminal — Mother AI message
> “Security override authorized. Staff evacuation in progress. Do not exit pod without permission.”

This message should contradict the player's experience: the terminal claims evacuation is in progress, yet the ship appears abandoned. Display it as diegetic terminal text and provide a subtitle/text equivalent.

### Cerebral — Late whisper
> “You’re not alone… but you’ll be fine.”

Use only after a quiet stretch, with an uncertain tone. Do not immediately show an enemy. The absence of a visual confirmation is the point.

### Cerebral — Hangar final
> “Disturbance detected. Take cover. Initiating shutdown protocols… Now!”

The line must not arrive so late that it becomes an unfair instruction. If the player cannot realistically take cover in the final sequence, change “Take cover” to a warning that fits the guaranteed escape beat.

### Additional short interaction lines (proposed)
These lines are design additions, not confirmed current dialogue:
- Pod code rejected: “Manual release denied. Consult the departure archive.”
- Power node 1/3: “Grid response detected. Two nodes remain.”
- Power restored: “Auxiliary grid stable. I did not initiate that movement.”
- Containment step complete: “Research channel isolated. Continue verification.”
- Crew recording found: “Recording archived. The speaker's identity is incomplete.”
- Hangar released: “Lockdown lifted. The cradle remains without power.”
- Ship power restored: “Cradle connection restored. Proceed to the cockpit.”
- Handoff: “Launch authorization accepted. Continue mission.”

Use captions for every spoken line. Voice synthesis is a fallback, not a reason to omit a text equivalent.

---

## 6. Quest Chain, Objectives and Rewards

| Quest | Objective / completion condition | Reward and progression | Failure protection |
|---|---|---|---|
| Q1. Wake from Unit 07 | Read/inspect the wall-chart clue and enter 2187 | Pod opens; Medical becomes reachable | Wrong code only resets input and shows feedback |
| Q2. Stabilize | Find and use the neural stabilizer | Stabilized state; unlocks the medical access-chip step | Re-interaction must not consume the item twice |
| Q3. Leave Medical | Recover access chip and reach the central deck | Bulkhead route opens; next objective appears | Chip and door state must persist for the current run |
| Q4. Restore facility power | Activate all three power nodes | Grid and relevant doors become available; robot reacts to the loud restore | Require all three unique nodes; display count |
| Q5. Investigate Research | Complete ISOLATE → VERIFY → PURGE; access archive | Research evidence/story progression | Wrong order must not silently count as complete |
| Q6. Recover Security access | Recover the crew recording and apply Security override | Hangar lockdown release enabled | If the recording is optional, do not falsely make it a hard gate |
| Q7. Open the hangar | Trigger manual lockdown release | Hangar route opens | Door state and objective update must agree |
| Q8. Reconnect ship power | Use the cradle hardline/coupler | Cockpit/ship boot becomes available | Coupler must not be interactable before its prerequisites |
| Q9. Reach spacecraft | Enter cockpit and launch | Prologue complete; original campaign loads | Handoff failure must provide retry/fallback, not a blank screen |

### Optional memory fragments
The README describes five optional memory fragments. They should:
- add context about the crew, research or ship;
- be clearly discoverable without obstructing the main route;
- provide a unique short text/audio payoff rather than a duplicate reward;
- never be required to finish the prologue unless the objective explicitly says so;
- not reset or block the main quest when collected in a different order.

No economy or combat upgrade reward is required in the prologue. Its rewards are tools, access, information, checkpoints and the launch transition.

---

## 7. Puzzles and Riddles

### Puzzle A — Hibernation magnetic lock (implemented; test required)
**Clue:** the console references the departure year and offers “READ DAMAGED WALL CHART.”  
**Solution:** 2187.  
**Interaction:** desktop keyboard digits / Enter / Backspace / Escape; mobile on-screen keypad.  
**Feedback:** wrong code shows an error and clears the entry; repeated failure explicitly points the player toward the wall chart.  
**Reward:** pod opens; quest advances.  
**Acceptance:** no bypass through desktop E, mobile wake, fallback paths, reset or pause handling.

### Puzzle B — Emergency power nodes (implemented; test required)
**Clue:** console labels and environmental signage point toward Maintenance and Research nodes.  
**Solution:** activate each unique node A, B and C.  
**Feedback:** count displayed as 1/3, 2/3, 3/3. Each node produces a distinct but related confirmation.  
**Reward:** grid state becomes active, access route opens and robot response may begin.  
**Acceptance:** duplicate interaction cannot increment twice; one missing node keeps the gate closed.

### Puzzle C — Research containment (implemented; test required)
**Clue:** visible console label “ISOLATE > VERIFY > PURGE.”  
**Solution:** activate the three protocol steps in order.  
**Feedback:** each step confirms the completed stage; out-of-order actions must be rejected or explain what is missing.  
**Reward:** archive becomes accessible.  
**Acceptance:** archive stays locked until all prerequisites are true; reset does not leave a partially false UI state.

### Puzzle D — Research color keypad (planned/reconcile)
**Clue from reference report:** “From warm to cool—follow the gradient.”  
**Solution from reference report:** Blue → Green → Red.  
**Reward:** research door opens; player can find the red keycard and scientist audio log.  
**Important:** this puzzle is not confirmed as the active implemented gate in the current nine-stage code. If added, it should gate entry to Research; do not make it conflict with the containment console inside.

### Puzzle E — Maintenance wiring panel (planned/reconcile)
**Clue:** a wall diagram shows mismatched wires and a note: “Match colors by symbol.”  
**Solution:** connect each symbol-labelled wire to its matching terminal using lever interactions.  
**Reward:** elevator/maintenance access and progression toward the hangar.  
**Acceptance:** each symbol needs a visible counterpart; do not make success depend on color alone. Provide icon/shape differences for color-vision accessibility.

### Puzzle rules
- Clues must be discoverable before or near the puzzle, not hidden in an unrelated optional fragment.
- Do not use pixel-perfect clicks on mobile.
- Wrong inputs give readable feedback and never softlock.
- Correct solutions produce both immediate feedback and an objective update.
- Puzzle UI pauses or safely isolates player movement while open.
- Provide a checkpoint or easy retry after each major gate.

---

## 8. Horror Events, Jumpscares and Safe-Fail Design

Horror should feel **very frightening through anticipation and sensory control**, not constant maximum volume. Use three major scripted peaks separated by quiet investigation, plus smaller environmental events. The player should feel hunted without being arbitrarily punished.

| Event | Trigger / setup | Intended effect | Player response and safe-fail | Status |
|---|---|---|---|---|
| Minor medical crash | Player enters Medical or turns away from a tool cart | A sharp metallic fall behind the player; no visible attacker | Harmless; must not repeat on every entry | Planned/verify |
| Scare 1: corridor robot | Player turns the marked corner after distant servo footsteps | Large inactive service robot slams through a door; loud impact and brief silhouette | Non-lethal. Nearby cover or sprint route; robot should not instantly catch the player | Reference event; implementation needs verification |
| Scare 2: vent drone | After a relevant lab/maintenance puzzle completes | Vent cover snaps open; drone drops/sweeps down with minimal warning | Crouch/cover can avoid the swing; hit causes brief stun, not death | Planned/reconcile |
| Maintenance activation | Successful wiring/power interaction | Sparks, relay snap and a robot's eye lights up behind the player | Player can sprint past or lead it toward a side door; pursuit rules remain fair | Power-reactive bot exists; exact authored beat needs verification |
| Blackout / comms disturbance | A designated story trigger, once per run | Ambient bed cuts out; one distant sound occurs; voice/static may interrupt | Player retains enough visibility/control to navigate; no forced blindness during a required puzzle | Trigger flags exist; exact timing needs playtest |
| Scare 3: hangar lunge | Final approach to escape hatch | Service/security robot lunges into foreground; brief mechanical stinger | Non-graphic and non-lethal; story cut/hatch opening guarantees survival | Reference event; implementation needs verification |
| Optional environmental dread | Observation/habitat spaces, if player explores | A distant silhouette/shadow movement or a sound from a space that appears empty | Never blocks the main objective; one-shot trigger; no fake chase unless AI can support it | Cue flags/areas exist; verify exact behavior |

### Scare choreography
1. **Establish a baseline:** hum, ventilation and distant hull noises.
2. **Remove a layer:** a hum stops, a light fails or footsteps briefly stop.
3. **Place the sound:** use a spatial source so the player can infer direction.
4. **Deliver the event:** a single clear visual/audio beat, not a chain of random effects.
5. **Give recovery time:** allow the player to regain orientation and hear a line or objective update.
6. **Change the situation:** the scare reveals a threat, alters a route, activates a robot or deepens the story.

### Robot fairness
- Robot awareness should use visible/sound-related conditions, not omniscience.
- Sprinting and noisy interactions can attract a robot; crouching and cover should reduce detection.
- Give the robot a readable state: patrol, investigate, search, pursue, recover.
- If the player breaks line of sight, the robot should investigate the last known location instead of snapping directly to the player.
- Stuns and catches must not permanently trap the player. Checkpoint/retry behavior must be reliable.
- Do not let a robot block the only interactable or sit inside a narrow door in a way that prevents progression.

### Reduced-scare mode
When enabled:
- reduce authored stinger intensity and harsh screen flashes;
- replace the strongest visual lunge with a milder movement or cut;
- preserve clues and quest progression;
- never remove an audio clue without providing a caption/text alternative;
- do not globally lower ordinary footsteps in a way that makes navigation confusing.

---

## 9. Sound Design Plan

### Ambient layers
- Low-frequency ship engine/air-system hum, subtle enough that players can listen for changes.
- Ventilation hiss, distant hull groans, occasional pipe ticks, electrical buzz and metal settling.
- Separate ambience for Medical, Central Deck, Research, Maintenance, Communications and Hangar. The hangar should sound larger and more reverberant than the medical rooms.

### Threat cues
- Metallic footsteps with direction and changing distance.
- Servo clicks and actuator strain before a robot becomes active.
- A rising static/heartbeat-like layer in the corridor, used sparingly.
- Intentional silence before major beats. Silence is a design event, not simply missing audio.
- Short stingers at the moment of impact only; do not run continuous horror music under every scene.

### Voice and logs
- Cerebral: controlled, clear, slightly close and internal; restrained pitch shift for whispers.
- Crew recordings: narrow-band radio/terminal processing, intelligible consonants, short static dropouts.
- All lines require subtitle equivalents. Include descriptions such as “[metallic crash behind you]” for important non-verbal cues.

### Technical requirements
- Use spatial audio for world sounds when practical and a mono fallback on low-power/mobile devices.
- Avoid many simultaneous loops. Fade unused layers and one-shot sounds.
- Keep ambience compressed enough for memory/performance while preserving voice clarity.
- Use separate master, ambience, voice and effects controls if the audio architecture supports them; the current UI's actual control mapping must be verified.
- Audio Comfort must lower peaks and bass without deleting navigation-critical information.

---

## 10. HUD, UX and Controls

### Visual language
- Muted steel grey, off-white and light amber; red is reserved for alarms/damage/critical warnings.
- Industrial monospace labels, concise objectives and subtle prompts.
- Avoid oversized neon UI, persistent quest panels or unnecessary pop-ups.
- The player's torch and the environment should do most of the visual work.

### Core information
- Current objective and a short instruction.
- Contextual interaction prompt only when an object is reachable.
- Subtitles for Cerebral and recordings.
- Subtle stamina/alert feedback; no oversized combat HUD in a walking-horror prologue.
- Clear puzzle feedback and visible state for multi-step tasks.

### Desktop input
- WASD: move.
- Mouse: look after pointer lock.
- E: interact.
- Shift: sprint, limited by stamina.
- Ctrl/C: crouch, according to the current control binding shown in the game.
- Escape: pause/close an overlay safely.
- Digits/Enter/Backspace: hibernation lock keypad.

**Implementation note:** Verify the exact crouch binding and any duplicate key bindings against the current HTML before release; the on-screen help must match the actual handlers.

### Mobile input
- Left-side virtual joystick: movement.
- Right-side drag region: camera look.
- Explicit touch wake/interact buttons.
- Dedicated crouch/sprint/torch/pause controls where shown.
- Touch buttons need large hit targets and must not overlap the look region.
- Prevent browser scrolling, text selection and accidental page zoom during gameplay.
- Releasing a touch, cancelling a pointer, switching tabs or opening pause must clear stuck movement/look input.

### Accessibility and safety
- Reduced jumpscare effects.
- Captions/subtitles.
- Voice on/off.
- Master volume and Audio Comfort.
- Content warning before the horror sequence.
- Brightness/contrast guidance for dark areas; do not make required objects invisible in reduced brightness.
- Keep puzzle solutions independent of sound alone and provide text alternatives for critical audio cues.

---

## 11. Pacing and Tension Timeline

The target curve alternates low-pressure exploration and high-pressure peaks.

| Approx. time | Intended beat | Tension |
|---|---|---|
| 00:00–02:00 | Pod awakening, clue inspection and 2187 lock | Low → rising |
| 02:00–05:00 | Medical stabilization, access chip and first environmental disturbance | Low → medium |
| 05:00–07:00 | Central deck footsteps and corridor robot event | High peak 1 |
| 07:00–10:00 | Three power nodes, investigation and short relief after each success | Medium, rising |
| 10:00–13:00 | Research containment, archive and scientist evidence | Medium → high |
| 13:00–15:00 | Crew recording and Security override | Emotional lull with unease |
| 15:00–17:00 | Hangar approach and final robot lunge | High peak 2/3 |
| 17:00–20:00 | Coupler, cockpit and launch transition | Resolution |

The exact placement should follow the actual route and playtest results. Do not force a scare merely because the timeline says one is due. If the player is still solving a required puzzle, finish the puzzle beat first.

---

## 12. Implementation Map and Scope Reconciliation

### Current prototype baseline
File: `prologue-addon/cerebral-prologue.html`
- Standalone Three.js first-person prologue.
- Nine objective stages from wake-up through cockpit launch.
- 2187 magnetic lock with wall-chart clue and touch keypad.
- Neural stabilizer, medical chip, three power nodes and Research containment sequence.
- Crew recording, Security override, hangar lockdown, ship cradle power and cockpit.
- Five optional memory fragments described by README.
- Robot movement/search/pursuit logic, hiding/decoy-related behavior and one-shot scare cue flags.
- Captions, Cerebral voice synthesis, reduced-scare/audio comfort settings and touch controls.
- Full-screen handoff to `../cerebral.html` through the prologue's campaign frame.

These are **source-level observations**, not a claim that each interaction has passed an end-to-end playthrough.

### Reference-report features to reconcile
1. Blue → Green → Red research door keypad.
2. Red keycard/audio log reward placement if that door is retained.
3. Symbol-and-wire maintenance panel.
4. Specific corridor, vent and hangar scare choreography.
5. Complete mapping of the report's exact Cerebral lines and Dr. Evans recording to unique triggers.
6. Per-zone ambience, silence transitions and spatial sound.
7. Measured target duration and 30 FPS mobile performance.
8. Content warning, brightness/contrast and final confirmation of all accessibility settings.

### Do not change
- Do not edit the protected `pass-1` branch.
- Do not replace the original `cerebral.html` campaign.
- Do not change spacecraft flight physics, weapons, targeting, shields, hacking, save system or campaign progression as part of prologue work.
- Do not turn Cerebral into a visible companion NPC.
- Do not add lethal random jumpscares or repeat scare rolls.
- Do not make optional memory fragments required without updating the quest design.
- Do not claim a feature is tested solely because its code or a smoke test exists.

---

## 13. Test and Acceptance Checklist

### Functional route
- [ ] Fresh start → read wall-chart clue → enter 2187 → wake.
- [ ] Incorrect code never releases the pod; repeated attempts remain recoverable.
- [ ] Medical stabilizer and access chip work once and update the correct objective.
- [ ] All three power nodes are required; each counts only once.
- [ ] Research containment steps work in order; archive remains locked until complete.
- [ ] Crew recording/Security interaction has correct prerequisites and clear feedback.
- [ ] Hangar lockdown opens; ship coupler is available only at the correct time.
- [ ] Cockpit launch loads the original campaign without overwriting saves.
- [ ] Restarting the prologue resets its temporary state cleanly.

### Horror and audio
- [ ] Each authored scare fires only at its intended trigger and at most once per run.
- [ ] No scare fires while a puzzle blocks movement or a menu is open.
- [ ] Reduced-scare mode softens designated events and leaves progression intact.
- [ ] Audio sources have sensible direction/volume; silence transitions are intentional.
- [ ] Every voice line has a subtitle; critical sounds have text descriptions.
- [ ] Robots investigate last known positions and cannot permanently block progress.

### Desktop and mobile
- [ ] Pointer lock and mouse look work; pause and focus changes release inputs.
- [ ] Joystick movement and right-side look are independent.
- [ ] Touch release/cancel and tab switching cannot leave movement stuck.
- [ ] All buttons are reachable in landscape and small portrait viewports.
- [ ] No browser scroll, text selection or zoom interrupts play.
- [ ] Collision prevents walking through walls, doors and large props.
- [ ] Objective text, keypad, subtitles and prompts remain readable without clipping.

### Performance and handoff
- [ ] Play from start to final handoff in desktop Chrome.
- [ ] Play the full route on a real Android device.
- [ ] Measure FPS on target hardware; target at least 30 FPS on supported mobile devices.
- [ ] Check memory and audio stability over a complete run.
- [ ] Test campaign handoff with no existing save and with existing saves.
- [ ] Confirm the original campaign remains unchanged and playable.

### Automated checks
The repository's Node smoke tests and GitHub Actions workflow provide source-level regression checks. Run locally from the repository root:

```bash
node --test prologue-addon/tests/prologue-smoke.test.mjs
```

Passing this command is necessary but not sufficient. Browser/device acceptance above must still be completed.

---

## 14. Prioritized Production Tasks

| Priority | Task | Completion evidence |
|---|---|---|
| P0 | End-to-end desktop playthrough and fix progression blockers | Recorded checklist with all nine objectives completed |
| P0 | Android touch playthrough: movement, look, keypad, pause and launch | Device-tested results; no stuck input |
| P0 | Verify campaign handoff and existing-save preservation | Test both new player and existing save states |
| P1 | Reconcile Blue → Green → Red door puzzle with current Research route | Puzzle is implemented, clued and tested, or explicitly removed from scope |
| P1 | Implement/decide symbol-wire panel | Working panel or documented scope decision |
| P1 | Author and verify the three major scare beats | Each trigger, warning, safe-fail and reduced-scare variant tested |
| P1 | Match dialogue/logs to actual events | Dialogue trigger checklist and subtitle coverage |
| P2 | Zone-specific ambience, silence and spatialization polish | Audio pass completed with headphones and mobile speaker |
| P2 | Accessibility pass: comfort mode, volume, captions, brightness/content warning | Each setting verified in gameplay |
| P2 | Measure and optimize frame time/memory | Actual target-device measurements; no invented performance claims |
| P3 | Refine environmental storytelling and optional fragments | Every fragment has unique text and does not block main quest |

---

## 15. Definition of Done

The prologue is ready for release only when:
1. A new player can complete the full route without external instructions.
2. Every mandatory puzzle has an in-world clue, clear feedback and a reliable retry.
3. The three major horror peaks are distinct, fair and correctly timed.
4. Cerebral's dialogue and crew logs appear at the right moments and are subtitled.
5. The full route works on desktop and Android, including keypad and pause/focus edge cases.
6. The prologue hands off to the original spacecraft campaign without changing campaign mechanics or damaging save data.
7. Automated checks pass, and the manual checklist has real browser/device results.
8. The README, this GDD, test report and error analysis agree about what is implemented and what remains open.

**Locked design principle:** Build dread with pacing, space, sound, withheld information and an intelligent-feeling ship. A scare should reveal something, change the player's understanding or force a meaningful response. If a feature competes with reliable controls, puzzle fairness, atmospheric quality, performance or the original spacecraft handoff, prioritize those core requirements.
