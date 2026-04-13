#!/bin/bash

set -euo pipefail

STATE=/var/lib/rspamd-learn/junk.stamp
NEW=$(mktemp)
trap 'rm -f "$NEW"' EXIT

# Capture the scan upper bound before walking Maildirs.
touch "$NEW"
[ -e "$STATE" ] || touch -d '1970-01-01' "$STATE"

shopt -s nullglob
maildirs=(/srv/dovecot/*/Maildir/.Junk/cur /srv/dovecot/*/Maildir/.Junk/new)

if [ "${#maildirs[@]}" -gt 0 ]; then
  find "${maildirs[@]}" -type f -newer "$STATE" -print0 \
    | xargs -0 -r -n1 -P4 bash -c '
        file="$1"
        rspamc learn_spam < "$file" >/dev/null 2>&1 || true
        rspamc -f 11 -w 10 fuzzy_add < "$file" >/dev/null 2>&1 || true
      ' bash
fi

mv "$NEW" "$STATE"
