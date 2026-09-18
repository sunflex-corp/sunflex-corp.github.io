# Addendum: migrated to dedicated `sunflex-corp` GitHub org

The site was originally deployed to `jiyou-eng/sunflex-site` (inside the same GitHub org as the
existing 지유이엔지 site) per the original design doc
(`2026-09-18-sunflex-site-launch-design.md`). After deploying, we discovered that
`jiyou-eng/jiyou-eng.github.io` has a custom domain bound (`jiyoueng.com`), and GitHub Pages
permanently redirects every `*.github.io` path in that account/org to the bound domain. So the
new SUNFLEX site was only reachable at `https://jiyoueng.com/sunflex-site/` — under the old
company's domain, which defeats the purpose of an independent brand.

Fix: created a new, fully separate GitHub org `sunflex-corp` and moved the site there as
`sunflex-corp/sunflex-corp.github.io` (the special repo-naming pattern for an org's root Pages
site). This serves at `https://sunflex-corp.github.io/` directly, with no path prefix and no
relation to `jiyoueng.com`.

The original `jiyou-eng/sunflex-site` repo and its local working copy at
`/Users/mac/Documents/지유이엔지/sunflex-site` were left untouched as a historical
reference/backup — not deleted. The new canonical working copy is
`/Users/mac/Documents/썬플렉스/sunflex-corp.github.io`, pushed to `sunflex-corp/sunflex-corp.github.io`.
