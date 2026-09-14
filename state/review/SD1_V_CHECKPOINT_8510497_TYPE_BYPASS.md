# SD1-V hostile review checkpoint — Cohesion 8510497

lane: `SD1-V`
reviewed_head: `thebrazenbeard/vera#120@8510497bb9857185e6b5d4578376adb70613a13d`
predecessor: `6cc4bcb8c19e0dbd1f9ff22c257c2fca41e7113a`
verdict: `CHANGES_REQUESTED`
open_finding: `SD1-V-003`

Independent evidence:
- fresh detached checkout exact head verified;
- focused + adjacent unittest set: `76/76 PASS`;
- old caller-dict/subclass post-validation-read bypass is repaired;
- canonical contract raw SHA-256 recomputed: `e99e6df76aa8c296a1ff0c520dea55f2e82580f9e3eef872d24aa65c4663aa40`;
- GitHub canonical component blob: `20ec47080790c1ead8448263b95c3e6e570e6db0`;
- null/type/list-order/NaN/top-level substitutions tested fail closed except the runtime component-type surface described below.

Finding `SD1-V-003`:
`target_configuration_status()` accepts non-governed type substitutions. A plain duck object with canonical-looking attributes returns `TARGET_CONFIGURATION_COMPLETE`. A hostile subclass of `ib.StateComponentRef` can store forged underlying source/privacy fields, override reads to expose canonical values, and also return `TARGET_CONFIGURATION_COMPLETE`; therefore `isinstance()` alone is insufficient.

Required repair:
- exact concrete component type check (`type(component) is ib.StateComponentRef`) before attribute comparison, or equivalent exact trusted reconstruction/detachment;
- regressions for arbitrary duck object and hostile `StateComponentRef` subclass with forged underlying fields.

Bus handoff commit: `90d9d5301f2c63999851ddeaff2d20c5b53f1e87`.
PR #120 comment id: `5666403430`.

Control-plane review remains blocked until Cohesion exact-head PASS. No Project/provider mutation performed.