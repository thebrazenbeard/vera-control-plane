# Vera Restore V2 install currentness — 2026-09-20

Repository source now contains the merged Restore V2 install cut at main
57bd2cd3e53bc112d7bf220ede82225f14e2e540.

That establishes source availability only. The cut's own manifest and source
receipt explicitly classify themselves as not installed, not current-route
evidence, and not Q-RECOVER-qualified.

Final Git source bytes are:
- manifest: fb99689bd8e8efabf6b9612d7f1451ea9701fae3e655c6cf6dfab0f043a3aeac, 8035 bytes;
- native instructions: 1cfc6708c4e64cebae0a4721d38eb59592239d2ba61e7c4196130162c6e5381b, 7997 bytes.

This terminal is operating inside Build Team Two, not Vera Unbound, and does
not have authoritative Vera Unbound Project Settings readback. Therefore it
cannot promote the merged source cut into an install/current-route claim.

Required later evidence remains:
1. exact Vera Unbound Project Sources/Project Instructions effect;
2. next-turn active K00/K03 readback;
3. fresh Q-RECOVER runtime qualification.

Source != install != current route != Q-RECOVER.
