# Robert Dong's academic website

A personalized [al-folio](https://github.com/alshedivat/al-folio) v1 site for **Yun (Robert) Dong**, Ph.D. student in Quantitative Biosciences at Georgia Tech.

The site has About, Research, Publications, and CV pages, your portrait, light and dark themes, and a downloadable CV. Content is ordinary Markdown, YAML, and BibTeX. No account system or database is needed.

## Publish on GitHub Pages

1. Create a public repository named **robyun.github.io** in your GitHub account. You may use another repository name if you prefer a project site.
2. Upload the contents of this source folder to the repository's `main` branch. If using the supplied ZIP, extract it first and upload its contents, including `.github/workflows/deploy.yml`; do not upload the ZIP itself. Keep the files at the repository root.
3. Open **Settings → Pages → Build and deployment**, and choose **GitHub Actions** as the source.
4. Open **Actions → Build and deploy academic website → Run workflow**. After the first successful deployment, later changes to `main` rebuild automatically.

For `robyun.github.io`, the public address will be **https://robyun.github.io/**. For a project repository, it will be **https://robyun.github.io/REPOSITORY/**. The workflow reads the repository path from GitHub Pages, so both work without source changes. The site address comes from `url` in `_config.yml`. For a custom domain, update that setting and your Pages domain.

This source has not been uploaded or published. The local template checkout retains its upstream Git history; the ZIP omits Git history and installed tools. Use your own new repository as the destination.

## Edit your site

On GitHub, open a content file, click the pencil, and commit the change. The site rebuilds automatically.

| What to update                                   | File                         |
| ------------------------------------------------ | ---------------------------- |
| Biography, research interests, profile caption   | `_pages/about.md`            |
| Research experience and capstone                 | `_pages/research.md`         |
| Publications page introduction                   | `_pages/publications.md`     |
| Papers, author lists, DOI links                  | `_bibliography/papers.bib`   |
| CV entries and downloadable CV content           | `_data/cv.yml`               |
| Email and social links                           | `_data/socials.yml`          |
| Site name, description, local URL, feature flags | `_config.yml`                |
| Profile photo                                    | `assets/img/robert-dong.jpg` |
| Colors, typography, spacing                      | `assets/css/main.scss`       |

Keep the `---` settings at the top of each Markdown page. Use `## Heading`, ordinary paragraphs, `-` for lists, and `[label](https://example.org)` for links.

The publications on the home page are entries with `selected = {true}` in the bibliography. All papers appear on the Publications page. Published author names and titles follow publisher records, including **Yun Dong**.

The web CV reads `_data/cv.yml`. Every GitHub deployment also regenerates the downloadable PDF from that same file. To regenerate it locally:

```sh
python -m pip install -r requirements-cv.txt
python scripts/export_cv.py
```

The biography is based on the supplied résumé. LinkedIn is linked, but its profile contents were not publicly accessible during setup. No advisor or lab affiliation has been inferred for your Ph.D. Personal phone and street address are omitted.

## Preview locally

Install Ruby 3.3 and Node.js 22, then run:

```sh
bundle install
npm ci
bundle exec jekyll serve
```

Open **http://localhost:4000/**. `_config.yml` defaults to your user-site address with an empty `baseurl`; The deployment workflow supplies the repository path; set the site address with `url`.

For a project-path smoke check:

```sh
bundle exec jekyll build --baseurl /al-folio
python scripts/check_site.py _site /al-folio
```

Windows users may need RubyInstaller with development tools and `bundle lock --add-platform x64-mingw-ucrt` before `bundle install`. GitHub's Linux runner uses the included upstream lockfile.

## Maintenance

```sh
npm run lint:prettier
bundle exec al-folio upgrade audit --no-fail
bundle exec jekyll build --baseurl /al-folio
```

Use `npx prettier . --write` to fix formatting. The template's Ruby dependency pins are retained; unused demo pages, demo assets, visual-test tooling, and maintenance workflows have been removed. Blog, search, comments, analytics, charts, and math are disabled until needed.

Two small theme overrides are intentional: `assets/css/main.scss` imports the upstream styles and adds visual adjustments; `_layouts/cv.liquid` adds a clearly labeled PDF link around the plugin-rendered CV. The CV rendering and interactive behavior remain in al-folio's versioned gems. `.al-folio-overrides.yml` records the upstream baseline; after updating gems, review `bundle exec al-folio upgrade overrides audit` before accepting a new baseline.

Based on upstream commit `929fbf71c5a45b13e9b5a20dfa425ce9e9de7935`. The MIT license and al-folio attribution are retained.
