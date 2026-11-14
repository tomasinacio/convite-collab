# Invitation site (static)

Generated folder: one page with hashed CSS, JavaScript, images and fonts. Every URL is relative, so it works at a root or a sub-path. Delete this README from the upload if you do not want it published.

## Build

```sh
.venv/bin/python -I comps/art/site_build.py [--base-url https://your-domain/]
```

The source is `comps/prototype.v15.src.html`. Run it again after any change.

## Deploy

| Host | Command | Account |
| --- | --- | --- |
| Cloudflare Pages | `wrangler pages deploy site` | free Cloudflare account, `wrangler login` once |
| GitHub Pages | publish the contents of `site/` | GitHub account; the repository is public on a free plan |
| Netlify | drag the `site/` folder onto the Netlify Drop page | free Netlify account |

`_headers` (long cache for hashed files, no cache for the page) works on Cloudflare Pages and Netlify; GitHub Pages ignores it.

## Unlisted, not private

`robots.txt`, a `noindex` meta tag and an `X-Robots-Tag` header keep search engines away. Anyone with the link can open it. Use an unguessable address, or Cloudflare Access if it must be private.

## RSVP later

The plan is Cloudflare Pages Functions plus D1. The site is already static-friendly: add a `functions/` folder next to `site/` and a form; nothing here has to change.

## Before a public launch

- Write the opening line. It shows `TODO(user) · frase de abertura` (and the English and Spanish versions) until then; the text is in the `kicker` entries of `app.js`, built from the source.
- Write the copy for any RSVP.
- Write the link-preview line: the description meta tag is still the prototype's note.
- Set the final domain and rebuild with `--base-url`; `og:image` must be an absolute URL.
