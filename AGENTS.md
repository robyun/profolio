# Working on Robert Dong's academic website

This is a personal site created from al-folio v1, not the upstream starter demo.

- Read `_config.yml` and the relevant content before editing. Prefer Markdown, `_data/*.yml`, and `_bibliography/papers.bib`.
- Do not invent publications, credentials, affiliations, or research results. Use supplied information and publisher records.
- Keep `Gemfile` and `_config.yml` plugin lists aligned. Runtime layouts and scripts belong to versioned al-folio gems; see `docs/BOUNDARIES.md` and `docs/ARCHITECTURE.md`.
- Intentional overrides are `assets/css/main.scss` and the tiny `_layouts/cv.liquid` wrapper for the labeled PDF link; track their baselines with `.al-folio-overrides.yml`. Keep CV rendering in its gem.
- The web CV and PDF both derive from `_data/cv.yml`. Run `python scripts/export_cv.py` after CV changes; deployment also regenerates it.
- Keep profile images optimized. Do not add personal phone numbers or street addresses by default.
- Validate with `npm ci`, `npm run lint:prettier`, `bundle exec al-folio upgrade audit --no-fail`, and `bundle exec jekyll build --baseurl /al-folio`.
- Preview representative pages at desktop and mobile widths after visual changes. The deployment workflow supports both root and project GitHub Pages addresses.
