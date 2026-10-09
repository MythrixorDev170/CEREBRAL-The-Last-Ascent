import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const htmlPath = fileURLToPath(new URL('../cerebral-prologue.html', import.meta.url));
const html = readFileSync(htmlPath, 'utf8');
const moduleMatch = html.match(/<script type="module">([\s\S]*?)<\/script>/);
assert.ok(moduleMatch, 'The playable prototype must have an embedded JavaScript module.');
const js = moduleMatch[1];

test('embedded JavaScript module passes Node syntax validation', () => {
  const dir = mkdtempSync(join(tmpdir(), 'cerebral-prologue-'));
  const file = join(dir, 'prologue.mjs');
  try {
    writeFileSync(file, js, 'utf8');
    const result = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8' });
    assert.equal(result.status, 0, result.stderr || result.stdout || 'node --check failed');
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('all statically referenced UI element IDs exist exactly once', () => {
  const declared = [...html.matchAll(/\bid=["']([^"']+)["']/g)].map(m => m[1]);
  const refs = [...js.matchAll(/\$\(['"]([^'"]+)['"]\)/g)].map(m => m[1]);
  const counts = new Map();
  for (const id of declared) counts.set(id, (counts.get(id) || 0) + 1);
  const missing = [...new Set(refs.filter(id => !counts.has(id)))];
  const duplicates = [...counts].filter(([, count]) => count > 1).map(([id]) => id);
  assert.deepEqual(missing, [], 'Missing DOM IDs referenced by $(): ' + missing.join(', '));
  assert.deepEqual(duplicates, [], 'Duplicate DOM IDs: ' + duplicates.join(', '));
});

test('all required accessibility and audio controls are present', () => {
  for (const id of ['settingsPanel', 'settingReducedScares', 'settingSubtitles', 'settingVoice', 'settingComfort', 'settingVolume', 'settingDone', 'openSettingsIntro', 'openSettingsPause']) {
    assert.ok(html.includes('id="' + id + '"'), 'Expected settings element ' + id);
  }
  assert.ok(js.includes("localStorage.setItem('cerebralPrologueSettings'"), 'Settings should persist locally');
  assert.ok(js.includes('style.opacity=subtitlesEnabled?1:0'), 'Captions must honor the subtitle setting');
  assert.ok(js.includes('voiceEnabled=gameSettings.voice!==false'), 'Voice playback must honor the saved preference');
});

test('reduced-scare mode is connected to startle feedback', () => {
  assert.ok(!js.includes('function scare()'), 'Unreachable generic scare helper should not remain in the code');
  assert.ok(js.includes('function scareTone('), 'Scare-only attenuation helper must exist');
  assert.ok(js.includes('const scaled=gameSettings.reducedScares?gain*.48:gain'), 'Reduced mode must soften tagged scare sounds');
  assert.ok(js.includes("scareTone(42,.45,'sawtooth',.075,wrecks[0].position)"), 'Authored scare cue must use the setting without affecting ordinary footsteps');
  assert.ok(js.includes('gameSettings.reducedScares?.45:1'), 'Wreck twitch motion should be reduced');
  assert.ok(js.includes("$('damage').style.opacity=gameSettings.reducedScares?.25:.72"), 'Reduced mode should soften the recovery flash');
});

test('mobile renderer pixel-ratio cap is consistent at startup and resize', () => {
  const count = html.split('isTouchDevice?1.0:1.5').length - 1;
  assert.equal(count, 2, 'Both renderer setup and resize must use the same 1.0 mobile cap');
});

test('nine quest stages and progression cap are internally represented', () => {
  const match = js.match(/const objectives=\[([\s\S]*?)\];/);
  assert.ok(match, 'Quest objectives array not found');
  const stageCount = [...match[1].matchAll(/\['[^']+','[^']+'\]/g)].length;
  assert.equal(stageCount, 9, 'Expected the current nine-stage prologue route');
  assert.ok(js.includes('Math.min(n,8)'), 'Quest index must stay within the objective array');
});

test('research sequence and three-node power gate are present', () => {
  for (const token of ['labIsolate', 'labVerify', 'labPurge', 'powerB', 'powerC', 'relayA', 'relayB', 'relayC']) {
    assert.ok(js.includes(token), 'Missing progression token: ' + token);
  }
  assert.ok(js.includes('if(count<3)'), 'Facility power must require all three nodes');
});

test('authored one-shot horror cues exist and random scare rolls stay removed', () => {
  for (const token of ['wreckScareA', 'wreckScareB', 'blackoutCue', 'commsCue']) {
    assert.ok(js.includes(token), 'Missing authored scare cue: ' + token);
  }
  assert.ok(js.includes('Random scare rolls intentionally removed'), 'Avoid reintroducing random scare spam');
});

test('touch controls keep movement, look, wake, and pause separately addressable', () => {
  for (const id of ['stickBase', 'lookPad', 'touchWake', 'touchInteract', 'touchCrouch', 'touchSprint', 'touchLight', 'touchPause']) {
    assert.ok(html.includes('id="' + id + '"'), 'Missing touch control: ' + id);
  }
  assert.ok(js.includes('wakeFromTouch'), 'Touch wake handler is required');
  assert.ok(js.includes("addEventListener('visibilitychange'"), 'Focus/visibility recovery handler is required');
});

test('the prologue hands off to the original campaign rather than replacing it', () => {
  assert.ok(html.includes('id="mainGameFrame"'), 'Original campaign iframe should remain available');
  assert.ok(js.includes('../cerebral.html'), 'Handoff should target the authoritative campaign entry');
  assert.ok(html.includes('Cerebral is only a voice') || html.includes('CEREBRAL is only a voice'), 'Story framing should keep Cerebral disembodied');
});

test('collision, robot search, doors, and waypoint systems remain present', () => {
  for (const token of ['function collidesAt(', 'function updateBots(', 'lastKnown', 'function updateDoors(', 'function updateWaypoint(']) {
    assert.ok(js.includes(token), 'Missing gameplay safety system: ' + token);
  }
});

test('browser preferences degrade safely when local storage or audio is unavailable', () => {
  assert.ok(js.includes('function readGameSettings(){try{'), 'Settings load should be guarded');
  assert.ok(js.includes('try{localStorage.setItem'), 'Settings save should be guarded');
  assert.ok(js.includes('if(audioCtx&&master)'), 'Audio setting application should tolerate missing Web Audio');
});

test('pod wake is gated by the documented 2187 magnetic lock', () => {
  for (const id of ['podLockPanel', 'podCodeDisplay', 'podKeypad', 'podReadChart', 'podChartClue', 'podEnter', 'podClear', 'podLater']) {
    assert.ok(html.includes('id="' + id + '"'), 'Missing pod-lock element: ' + id);
  }
  assert.ok(html.includes('>2187</strong>'), 'Departure-year clue must be available in the wall-chart readout');
  assert.ok(js.includes("if(podCodeBuffer==='2187')"), 'Only the intended four-digit code should release the pod');
  assert.ok(js.includes("if(a==='wake'&&step===0){openPodLock();return}"), 'Desktop interaction must open the lock instead of releasing immediately');
  assert.ok(js.includes("if(wake){interact(wake)}else{openPodLock()}"), 'Mobile fallback must not bypass the lock');
  assert.ok(js.includes("if(!started||paused||launch||podLockOpen)return"), 'Gameplay updates should pause while the keypad is open');
});
