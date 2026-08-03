#!/usr/bin/env bash
# SessionStart hook: resolve the configured authorship identity and inject it as
# context, or nudge the agent to run the one-time setup dialog.
#
# Config file: ${XDG_CONFIG_HOME:-~/.config}/mai/authorship
#   mode=git      resolve from `git config` at session time (follows per-repo overrides)
#   mode=custom   use the name= and email= lines below
#   name=<display name>
#   email=<address>
#
# Format is one key=value per line, no spaces around the '='. Unknown keys and
# comment lines are ignored.
set -u

config="${XDG_CONFIG_HOME:-$HOME/.config}/mai/authorship"

nudge_and_exit() {
  echo "AUTHORSHIP: not configured. Before writing any author, copyright, or credit field, run the /authorship-setup dialog once."
  exit 0
}

[ -f "$config" ] || nudge_and_exit

mode=""
name=""
email=""

while IFS='=' read -r key value || [ -n "${key:-}" ]; do
  case "$key" in
    mode) mode="$value" ;;
    name) name="$value" ;;
    email) email="$value" ;;
  esac
done < "$config"

if [ "$mode" = "git" ]; then
  name="$(git config user.name 2>/dev/null || true)"
  email="$(git config user.email 2>/dev/null || true)"
fi

[ -n "$name" ] || nudge_and_exit

if [ -n "$email" ]; then
  echo "AUTHORSHIP: $name <$email>"
else
  echo "AUTHORSHIP: $name (no email configured - omit the address rather than inventing one)"
fi

exit 0
