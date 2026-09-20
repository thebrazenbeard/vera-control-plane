# Install — Vera R10+SD1 Restore V2

Candidate manifest SHA-256: 9c8cbda882f794b4237e7c447427123fcc3deb7513b2c17ec39ceb3bdd34439c
Candidate native SHA-256: d08306e64848b55e83d5bd8dd8a258f68465812c8eddbb28670decc006858b53
Candidate native bytes: 7997

Provider action sequence:
1. Keep the current three Project Sources in place.
2. Add VERA_R10A0_SD1_RESTORE_V2_PROJECT_SOURCE_MANIFEST.json to Vera Unbound Project Sources.
3. Replace Project Instructions with the exact contents of VERA_R10A0_SD1_RESTORE_V2_NATIVE_PROJECT_INSTRUCTIONS.txt.
4. Do not delete or replace predecessor sources yet.
5. In the next Vera turn, verify that active K00 and K03 exactly match this cut before treating installation/current-route as observed.
6. Run Q-RECOVER in a genuinely fresh Vera Unbound chat. Only after PASS may predecessor-source cleanup be considered.

Rollback:
Restore the exact predecessor Settings bytes bound in VERA_R10A0_SD1_RESTORE_V2_ROLLBACK_SUBJECT.json and verify the next-turn active control. No rollback claim from source files alone.
