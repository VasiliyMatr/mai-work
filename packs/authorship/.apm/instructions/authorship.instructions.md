---
description: Resolve one authorship identity from user configuration and use it for every author, copyright, and credit field.
---

# Authorship

## The identity

The `SessionStart` hook injects a line of the form:

```
AUTHORSHIP: <name> <<email>>
```

Use that exact string wherever a work needs attribution. Include the email
whenever the field's format allows it.

If the line says `not configured`, run the `/authorship-setup` dialog before
writing any attribution field.

## No hook available

Harnesses without hook support (OpenCode) receive no `AUTHORSHIP:` line. Resolve
it yourself, in this order:

1. Read `${XDG_CONFIG_HOME:-~/.config}/mai/authorship`. If `mode=custom`, use its
   `name` and `email`. If `mode=git`, continue to step 2.
2. Run `git config user.name` and `git config user.email`.
3. If neither resolves, ask the user rather than guessing.

## Where it applies

`author` fields in package manifests, plugin metadata, copyright headers, LICENSE
files, commit authorship, README credits, and any other attribution field.

## Rules

- One identity, one spelling. Never vary the form by context.
- Never substitute an account handle, username, or nickname for the configured
  name. A handle belongs in prose - a README line, a profile link - not in an
  `author` or `copyright` field.
- Never invent an email address. If none is configured, omit it.
- Do not overwrite an existing copyright holder in a file you did not author.
