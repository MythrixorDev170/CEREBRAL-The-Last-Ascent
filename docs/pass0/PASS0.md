# Pass 0 – safety net (infrastructure only; no gameplay, visual, control or flight changes)

- **Flight lock:** 7 regions in `cerebral.html` fenced by `// === FLIGHT LOCK BEGIN: <name> ===` / `// === FLIGHT LOCK END ===` (tune, evade, mouse-steering, touch-stick, steering-curve, movement, camera). Their text plus fingerprints of `ss()`, `cl()`, default WASD bindings and default steering settings is hashed (cyrb53) and compared with `FLIGHT_LOCK_HASH`. A deliberate flight change must be re-sealed with `node pass0/pass0_tests.js seal`.
- **TUNE:** 56 constants, values identical to the originals (`TUNE_TABLE.md`). **PAL:** 36 entries, identical to the former literals.
- **Save schema:** `saveVersion: 1` on new saves. Saves without the field are legacy v0 and still load; saves with a version newer than 1 are ignored, not overwritten.
- **Test hook:** `window.CER_TEST.run(script,{seed})` drives the normal action path (`press/release`, `mo`, `mv`) through the real `play(dt)`.
- **Debug overlay:** open the page with `?perf=1`. Nothing is created without it.
- **Dead code:** `ghost()` and `jump()` removed (no executable references, found with an AST parser, `deadcode.js`). `warn2()` kept: it has a live call site (counter-hack warning).
- **Run:** `cd pass0 && npm i && python3 pass0_build.py && npm run seal && npm test` (needs three@0.128.0 and acorn). Results: `pass0_results.json`.