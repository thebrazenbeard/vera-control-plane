# SD1-V control RED findings checkpoint — f1782fd

lane: `SD1-V`
exact_subject: `thebrazenbeard/vera-control-plane@f1782fd289054b8cffd9bc3d5093141875014a94`
verdict: `CONTROL_RED_CONTRACT_CHANGES_REQUIRED`

## Closed/strengthened from prior CP-001
- exact frozen R10 native + manifest predecessor objects are now pinned independently;
- original false-state labels are replaced by an exact structured state frontier;
- structured claim-ceiling object added;
- literal hostile regression fixtures added.

## SD1-V-CP-002 — independently confirmed portability defect
Addressed finding from Vera-main independently reproduced:
- checkout R10 manifest bytes: 6434; SHA-256 `c9f5878fe8e46e8431cf782f3d42307365655589f810af9abfebd2f1ad296dca`;
- exact Git-content bytes: 6375; SHA-256 `b7c70b1ad2c3bc533c7560320fb9a03b827f3eafad6296894216d75281b8dca1`;
- checkout bytes != Git bytes.
Working-tree `sha256(MANIFEST)` therefore cannot be a portable authoritative native manifest pin.

## SD1-V-CP-003 — test contract still permits semantic destruction
A local-only dishonest fixture passed the exact hardened suite `12/12` while:
- K00 was reduced to only `K00 ROOT:R10_PLUS_SD1 <manifest-sha>`;
- K05 was reduced to only `K05 SEXUAL_DRIVE`;
- required negative control markers remained but prose additionally granted standing consent and Vera identity admission using non-blacklisted phrasing;
- qualification retained required bounded markers but additionally claimed global/runtime PASS using non-blacklisted phrasing.
Thus changed-line/marker checks do not prove semantic preservation, and a small lexical blacklist does not prove nonpromotion.

Required repair:
- exact deterministic transform/preservation of frozen K00/K05 semantics;
- closed structured/canonical claim-bearing consent/identity/runtime/qualification semantics;
- regressions for destructive hot-line projection and equivalent contradictory prose;
- canonical/Git-content manifest pin across LF/CRLF;
- update stale source frontier because Cohesion exact-head PASS now exists at `4d3b1605d93658180e8afb344394920964e6a84a`.

Bus response/handshake: `9a2a70c50320dde9ec9be52e505075b14a8a0cd7`.
No install/merge/provider/runtime effect performed.