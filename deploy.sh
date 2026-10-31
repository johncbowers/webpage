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

rsync -e "ssh -J bowersjc@util.cs.jmu.edu" -a -i \
  --chmod=Du=rwx,Dgo=rx,Fu=rw,Fgo=r \
  --exclude .DS_Store \
  "$@" \
  site/ bowersjc@w3.cs.jmu.edu:/home/bowersjc/public_html/
