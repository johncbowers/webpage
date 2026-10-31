# John C. Bowers

Source for https://w3.cs.jmu.edu/bowersjc/, built with
[Zensical](https://zensical.org) like the department's
[research](https://w3.cs.jmu.edu/research/) and
[research talks](https://w3.cs.jmu.edu/research-talks/) sites.

Ported in 2026-10 from the old Metalsmith site (`FacultyPage2018/metalsmith`
in iCloud). Page text is unchanged; the only edits to the Markdown are
front matter (`template:` dropped), a `# Bio` heading on the home page, and
`markdown` attributes on `<figure>`/`<figcaption>` so caption links render.

## Layout

- `docs/*.md`: one file per page. `use_directory_urls = false` keeps the old
  URLs (`activity.html`, `publications.html`, ...).
- `docs/images/`: images and posters, same paths as before.
- `overrides/partials/bio.html`: the left sidebar (portrait, office hours,
  teaching, contact). Update office hours and teaching each semester.
- `overrides/main.html`: puts the bio in the sidebar, and under the home page
  on phones.
- `docs/stylesheets/extra.css`: JMU purple/gold, shared look with the
  department sites.

## Building locally

```
python3 -m venv .venv && .venv/bin/pip install 'zensical==0.0.*'
.venv/bin/zensical serve      # http://localhost:8000/bowersjc/
```

## Deploying

```
./deploy.sh --dry-run   # what would change
./deploy.sh             # build and rsync site/ to ~/public_html via stu.cs.jmu.edu
```

The rsync never deletes: `public_html` also holds `files/`, `fya/`,
`chord_graph/` and older pages that this repo doesn't build.

## Checking links

```
.venv/bin/zensical build --clean && python3 -I scripts/check_links.py
```

Dead outside links get a DOI, the page's new address, or a Wayback Machine
copy (`https://web.archive.org/web/<timestamp>/<old url>`), never a guess.
