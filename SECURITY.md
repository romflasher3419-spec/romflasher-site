# Security policy

## Supported versions

The site is rebuilt from `main` on every push. Only the current live deployment
at <https://romflasher.in> is supported.

| Version | Supported |
| --- | --- |
| Live site (`main`) | Yes |
| Older commits / forks | No |

## Reporting a problem

Please report security issues privately rather than in a public issue:

- Use the contact form at <https://romflasher.in/contact.html>, or
- Email **vrohit3419@gmail.com** with the subject `SECURITY`.

Include the URL, what you found, and the smallest set of steps that reproduces
it. I aim to acknowledge reports within 72 hours and to ship a fix or a clear
mitigation within 7 days for anything that affects visitors.

Please do not run destructive tests against the live site, and do not access
data that is not yours.

## What is in scope

- Cross-site scripting, HTML injection or open redirects on this site
- Leaked secrets, tokens or private keys in the repository or build output
- Supply-chain problems in the build and deploy workflow
- Malicious or unexpected behaviour in the Android APK published from
  `romflasher3419-spec/rom-flasher-tool`

## What is out of scope

- Reports that only say a security header is missing without a working impact
- Missing DMARC/SPF records on a domain that does not send mail
- Rate limiting or spam on third-party services (FormSubmit, GitHub, YouTube)
- Vulnerabilities in Android, a ROM, Magisk, KernelSU or a vendor firmware
  package linked from a guide

## How the live site is protected

- HTTPS is served by GitHub Pages with a Let's Encrypt certificate for
  `romflasher.in`, the canonical host.
- The site is static: there is no server-side code, database, login or file
  upload, so there is no application server to compromise.
- Analytics and AdSense load only after an explicit consent choice. Google
  Consent Mode v2 defaults are set to `denied` before any request is made.
- The contact form posts to FormSubmit with its server-side CAPTCHA enabled and
  a honeypot field; the site itself never stores submissions.
- Outbound download links carry `rel="nofollow noopener"`.
- The APK is signed (v2 + v3, RSA 4096) and its SHA-256 is published on the
  download page.
- `dist/_headers` is generated with HSTS, CSP, `X-Frame-Options`,
  `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` and COOP.
  GitHub Pages ignores `_headers`; the file is ready for a host that applies it
  (Cloudflare Pages or Netlify).

## Dependency and secret hygiene

- The site build uses only the Python standard library, so there is no runtime
  dependency tree to patch.
- GitHub Actions are pinned to major versions and watched by Dependabot.
- `ROMFLASHER_*` values are repository variables, never committed secrets. No
  token, password or private key belongs in this repository.
