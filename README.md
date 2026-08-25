# Nathan Achinger

Personal portfolio site at [nathanachinger.github.io](https://nathanachinger.github.io), built with [Jekyll](https://jekyllrb.com) and the [Academic Pages](https://github.com/academicpages/academicpages.github.io) theme (MIT, a fork of [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/)).

## Run locally

```bash
bundle install
bundle exec jekyll serve -l -H localhost
```

Then open [http://localhost:4000](http://localhost:4000). Changes to Markdown and HTML rebuild automatically; restart the server after editing `_config.yml`.

## Add a project

1. Create `_projects/my-new-project.md`
2. Use this front matter:

```yaml
---
title: "My New Project"
excerpt: "One-line summary."
collection: projects
---
```

3. Write the page body in Markdown.

It will show up on [/projects/](https://nathanachinger.github.io/projects/) with no nav or config changes.

## Resume

Place your PDF at `files/resume.pdf`. The top-bar Resume link points there.

## LinkedIn

Replace `YOUR-LINKEDIN-USERNAME` in `_data/navigation.yml` and `_config.yml`.
