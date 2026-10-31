#!/bin/bash
# Build the site and copy it to w3.cs.jmu.edu/bowersjc (~/public_html).
#   ./deploy.sh --dry-run   show what would change, copy nothing
#   ./deploy.sh             publish
#
# No --delete: public_html also holds things this repo doesn't build
# (files/, fya/, chord_graph/, page/, the older publications/ site, ...).
set -euo pipefail
cd "$(dirname "$0")"

ZENSICAL=zensical
[ -x .venv/bin/zensical ] && ZENSICAL=.venv/bin/zensical
"$ZENSICAL" build --clean

# Jump host. stu, because util can't reach w3 on port 22 (2026-10-30).
# Override if that changes: JUMP=bowersjc@util.cs.jmu.edu ./deploy.sh
JUMP="${JUMP:-bowersjc@stu.cs.jmu.edu}"

rsync -e "ssh -J $JUMP" -a -i \
  --chmod=Du=rwx,Dgo=rx,Fu=rw,Fgo=r \
  --exclude .DS_Store \
  "$@" \
  site/ bowersjc@w3.cs.jmu.edu:/home/bowersjc/public_html/
