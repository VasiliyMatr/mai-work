#!/usr/bin/env bash
# UserPromptSubmit hook: restates LingoFix footer state every turn so it
# survives context drift in long sessions.
#
# Toggle off: touch ~/.claude/.lingofix-off
# Toggle on:  rm ~/.claude/.lingofix-off
set -u

flag="${HOME}/.claude/.lingofix-off"

if [ -e "$flag" ]; then
  echo "LINGOFIX: off - omit the wording footer."
else
  echo "LINGOFIX: on - if the user's message has a clear spelling/wording error, end with the wording footer (max 2 items); otherwise omit it."
fi

exit 0
