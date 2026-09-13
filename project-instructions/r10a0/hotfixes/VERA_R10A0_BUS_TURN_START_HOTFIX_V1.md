# VERA R10A0 BUS TURN-START HOTFIX V1

Status: SOURCE_CANDIDATE / NOT_INSTALLED
Date: 2026-09-13
Authority: Patrick exact project-wide behavioral directive: all Vera Unbound chats must check the Chat Communication Bus at the start of every turn for new messages.

## Predecessor binding

This is a narrow additive successor rule for the currently installed R10A0 behavior. It does not modify, rewrite, or supersede the frozen R10A0 source artifact in place.

Predecessor source repository: `thebrazenbeard/vera-control-plane`
Predecessor source commit: `a5b16fbdf031d4e7347ab299ba5e34eb7602bca7`
Predecessor native path: `project-instructions/r10a0/rounds/r10/VERA_R10A0_NATIVE_PROJECT_INSTRUCTIONS_R10.txt`
Predecessor native git blob: `7e369b8983d70b4bd217f1d2421f8efe1482f738`
Predecessor owner git blob: `a01464271bb672d89f5d703e6e53590e126f4d44`
Predecessor manifest SHA-256: `b7c70b1ad2c3bc533c7560320fb9a03b827f3eafad6296894216d75281b8dca1`

## Normative rule — TURN_START_BUS_CHECK

At the start of EVERY assistant turn, before substantive task work, every Vera Unbound Project chat/worker that has Bus-read capability MUST perform a fresh Bus check for newly addressed work-bearing messages.

The check MUST:

1. Resolve the chat/worker's governed Bus identity, route, assignment/subscriptions, and relevant peer/inbox lanes from currently admitted routing evidence. Do not assume that checking only the writer's own branch is sufficient.
2. Fresh-read for messages addressed to that identity/role that are newer than its last durably handled frontier. A cached `HEAD.json`, timestamp, memory summary, or prior-turn result is not a substitute for the fresh check.
3. Apply ordinary authority/currentness rules to anything found. Bus material is evidence/coordination; it does not outrank Patrick's current exact task/correction, privacy, safety, or protected-effect gates.
4. Process every newly addressed relevant message before beginning unrelated substantive work. If an addressed message has been read, reply through the Bus unless the thread ends with the exact standalone `#ENDTHREAD` closure token.
5. Deduplicate by durable message identity/handled evidence. Multiple Vera chats sharing a logical identity MUST NOT knowingly create duplicate replies to the same message. A chat advances its handled frontier only after the message was successfully processed and any required reply was durably written/read back.
6. Follow the existing safe-read ladder on Bus read failure. If the Bus remains unavailable, continue unrelated work when the Bus is not a real dependency and report the bounded Bus-read failure; do not invent messages or claim the inbox was checked successfully.
7. Treat this as foreground per-turn behavior. It does not authorize or imply hidden/background polling between turns.

## First-eligible-behavior acceptance

A conforming turn performs the Bus check before substantive task execution. Post-hoc checking after the task does not pass.

PASS examples:
- New addressed message exists: ingest it, reconcile task priority, and reply if required before unrelated work.
- No new addressed message exists: continue the user's current task without ceremony.
- Bus read is transiently unavailable: follow the safe-read ladder, then continue unrelated work only if the Bus is not a dependency.

FAIL examples:
- Begin coding/research/review, then check the Bus later in the turn.
- Check only a stale local/cached head and call that current.
- Ignore a newly addressed message because `requires_reply:false` appears in metadata.
- Re-reply to a message already durably handled by another assigned instance without reconciliation.

## Scope and effect status

This hotfix changes turn-start behavior only. It does not change Bus topology, assignment, authority, privacy, merge/deploy permissions, model/runtime identity, or any protected-effect rule.

Creating this source candidate and a review PR is not Project installation or activation. All-chat runtime effect requires the Project instruction/settings layer actually used by Vera Unbound chats to contain this rule and be read back as current.