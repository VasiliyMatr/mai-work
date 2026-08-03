---
description: One-time dialog that records which identity to use for authorship, copyright, and credit fields.
---

Configure the authorship identity for this user. This is a one-time setup; the
result is stored outside any repository and applies to every project.

## 1. Read the current state

```bash
git config user.name
git config user.email
cat "${XDG_CONFIG_HOME:-$HOME/.config}/mai/authorship" 2>/dev/null
```

If a config already exists, show it and confirm the user wants to change it
before continuing.

## 2. Ask

Present exactly two choices, with the resolved git identity substituted into the
first label:

- **Use git user: `<name> <email>` (Recommended)** - authorship follows
  `git config` at session time, so a per-repository override is picked up
  automatically.
- **Set a different name** - ask for the display name, then the email address.
  An empty email is allowed; the identity is then name-only.

If `git config user.name` is unset, say so and offer only the second choice.

## 3. Write

Create `${XDG_CONFIG_HOME:-$HOME/.config}/mai/authorship`, creating the parent
directory if needed. One key=value per line, no spaces around the `=`.

For the git option, write only the mode - the name is resolved at session time,
so storing it here would let it go stale:

```
mode=git
```

For a custom identity, write all three keys:

```
mode=custom
name=Ada Lovelace
email=ada@example.com
```

Omit the `email` line entirely when the user gave no address.

## 4. Confirm

Run the hook to show what will be injected from now on:

```bash
bash .claude/hooks/authorship/.apm/hooks/authorship-context.sh
```

Report the resolved identity and note that it takes effect in the next session,
since the hook runs at `SessionStart`.
