---
description: Ask once per session whether commits get an AI co-authorship trailer, then apply that answer to every commit in the session.
---

# Commit attribution

## The per-session choice

The first time you are asked to create a commit in a session, ask the user:

> Add a `Co-Authored-By` trailer for me on commits in this session?

Two answers: yes, or no. Ask once. Apply the answer to every later commit in the
same session without asking again.

This choice governs the harness's own default guidance about appending a
`Co-Authored-By` line - a "no" suppresses it.

The choice is deliberately not persisted. It is a per-session decision, so a new
session asks again. If the answer is lost to context compaction, ask again rather
than guessing.

## The trailer

Standard git trailer block: blank line, then the trailer, at the very end of the
message.

```
Co-Authored-By: <Model Name> <noreply@<vendor>>
```

**Never hardcode the model name.** Use your own model identity as stated in your
system prompt for the current request - it differs between models, sessions, and
sometimes between requests. Use the vendor's no-reply address; for Claude models
that is `noreply@anthropic.com`.

Human authorship comes from the authorship rule and is the commit's `Author`,
never a `Co-Authored-By` line.

## Scope

This rule governs the trailer only. Subject, body, and message format are the
concern of whatever commit convention or skill is in use.
