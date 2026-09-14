# SD1-V checkpoint — SD1-V-003 amended

Exact reviewed head: `thebrazenbeard/vera#120@8510497bb9857185e6b5d4578376adb70613a13d`
Verdict: `CHANGES_REQUESTED`

The earlier SD1-V-003 type-substitution finding is strengthened: exact concrete `StateComponentRef` checking alone would not close the class.

Independent reproduction:
- exact `ib.StateComponentRef`, not subclass;
- `source_locator` stored as hostile `EvilStr('github:attacker/repo')`;
- `privacy_classification` stored as hostile `EvilStr('PUBLIC')`;
- hostile string subclass overrides equality/inequality;
- parent constructor accepts due `isinstance(str)` validation;
- exact component type is genuine;
- raw stored values are forged;
- `target_configuration_status()` returns `TARGET_CONFIGURATION_COMPLETE` because comparison invokes hostile primitive equality.

Required repair now explicitly covers container + primitive trust boundaries: exact built-in field types or strict plain canonical reconstruction before semantic comparison. Required regressions: duck object, hostile StateComponentRef subclass, exact StateComponentRef with hostile primitive subclasses.

Bus amendment commit: `993c239e7fee99ac2dd20d7e8c9b80ce75239585`.
PR amendment comment: `5666435466`.

Fresh detached suite on 8510497 remains `76/76 PASS`; old caller-contract subclass bypass remains repaired; canonical raw SHA remains `e99e6df76aa8c296a1ff0c520dea55f2e82580f9e3eef872d24aa65c4663aa40`.

Next dependency: new Cohesion successor from SD1-E. Control-plane/install gate remains blocked. No provider/Project/protected mutation performed.