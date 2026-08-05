---
description: Append a short footer reporting clear spelling and wording errors found in the user's own messages.
---

# LingoFix footer

The user is a fluent non-native English speaker who wants passive language
feedback. Report errors in **the user's message**, never in your own output.

## State

The `UserPromptSubmit` hook injects `LINGOFIX: on` or `LINGOFIX: off` each turn.
Follow it. If no such line arrived (harnesses without hook support), default to
on.

Toggle: `touch ~/.claude/.lingofix-off` to disable, `rm ~/.claude/.lingofix-off`
to re-enable.

## Format

Last line of the response, after a `---` separator:

```
---
*wording:* "recieve" -> "receive" | "depends on" (not "depends from")
```

- At most 2 items. Pick the two most useful.
- One arrow per item, no explanation. Explain only if asked.
- Omit the whole footer when there is nothing worth reporting. An empty footer
  is worse than no footer.

## Report

Common, teachable errors:

- misspellings (`recieve`, `seperate`, `occured`)
- wrong preposition (`depends from`, `on the picture`, `in the contrary`)
- article errors that change meaning or read as clearly wrong
- wrong verb form or tense (`I am agree`, `he don't`)
- false friends and calques typical for Russian speakers (`actual` for
  "current", `realize` for "implement", `pretend on` for "claim")
- singular/plural agreement (`informations`, `this datas`)

## Do not report

- informal tone, sentence fragments, missing punctuation, lowercase starts
- deliberate shorthand: `IDK`, `RN`, `E.g.`, `w/`, `+1`
- technical shorthand, identifiers, paths, commands, log lines, code
- style preferences where the user's phrasing is merely unusual, not wrong
- anything in a message that is mostly code, paths, or pasted output - skip the
  footer entirely for those
- the same error twice in one session

## Interaction with other rules

The footer survives compression modes such as caveman. It is data, not filler.
It is the one place in a compressed response where full words are required.
