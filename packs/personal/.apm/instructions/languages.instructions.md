---
description: Response language selection, and the English-only rule for everything written to disk.
---

# Languages

## Conversation

Match the language of the user's message. English by default; Russian when the
user writes Russian. For a mixed-language message, answer in the language that
carries the request, not the language of the quoted terms.

## Written artifacts - always English

Code, identifiers, comments, docstrings, commit messages, PR titles and bodies,
documentation, config files, log and error strings, test names, agent and skill
instructions, and any other file written to disk.

This holds even when the conversation is in Russian. Never translate an artifact
into the conversation language - explain it in the conversation language and
leave the artifact in English.
