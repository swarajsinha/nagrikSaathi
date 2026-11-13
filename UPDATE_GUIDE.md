# Nagrik Saathi — Update Guide
- Records: `content/schemes|documents|scams/*.json`, `content/helplines.json`, `content/updates.json` (What's New). One record = one page/entry.
- Page text for tabs (Rights, About, Privacy...) is in `build.py`; shared look in `assets/site.css`, behaviour in `assets/app.js`.
- Mark `status` = `verified` and set `last_verified` (YYYY-MM-DD) ONLY after a genuine official-source check. Never change it just for a redeploy. High-risk fields (eligibility, amounts, deadlines, pension, legal rules) need a second reviewer.
- Build: `python3 build.py` (डोमेन पहले से https://nagriksaathi.in सेट है; बदलना हो तो SITE_URL दें) -> `dist/` (sitemap, robots, search-index, _headers generated). Update `TODAY` in build.py for accurate lastmod.
- Deploy: Cloudflare Pages, build command `python3 build.py`, output `dist` (SITE_URL env var अब ज़रूरी नहीं).
- Rollback: revert the Git commit and redeploy (Pages keeps old deployments).

## Automatic change detection (monitor)
- `monitor/monitor.py` fetches each record's `source_url`, compares a hash with `monitor/snapshots.json`, and writes `monitor/report.json`.
- On a change it ONLY flips a `verified` record to `pending` (🟡) and adds `change_note`. It never edits benefit amounts, eligibility or dates.
- Sites that forbid automated access (robots.txt) are listed under `manual_check`; check those by hand.
- `.github/workflows/monitor.yml` runs it daily on GitHub Actions (free) and opens a GitHub Issue when something needs review. Requires the project in a GitHub repo.
- A page hash change can be just a banner/date change; a human decides whether the facts really changed.

## Outbound links
- Government / source links: use `ext()` (`rel="noopener noreferrer"`) — our site is not revealed to them.
- A link to a promoted business, maker or creator: use `bext()` (`rel="noopener"`, no `noreferrer`). Keep their official URL exactly as published; never add `?ref=` / UTM / tracking codes.
- Site-wide referrer policy `strict-origin-when-cross-origin` is set in `_headers` and as a `<meta>` in every page (sends only our site address, never the page path).
- When the first business link is added, also add to the Privacy page: "When you open a business link from our website, your browser tells that business only that the visit came from our website address. We do not share anything else about you." (Hindi: "जब आप हमारी वेबसाइट से किसी व्यवसाय का लिंक खोलते हैं, तो आपका ब्राउज़र उस व्यवसाय को केवल इतना बताता है कि आप हमारी वेबसाइट से आए हैं। हम आपके बारे में और कुछ साझा नहीं करते।")

## Publishing rule: only 🟢 is shown
`build.py` publishes only records with `"status": "verified"` (schemes, documents, scams) and only verified helplines.
Records marked `pending` or `unverified` stay in `content/` as drafts but are NOT built into the site, hub pages, search index, finder or sitemap.
To publish a draft: verify it against an official source, set `status` to `verified`, fill `last_verified`, rebuild.


## तारीख़ें, अपने आप हटना और "क्या नया है?" (12 नवंबर 2026)
- **साइट का अंतिम अपडेट** हर पेज के नीचे और होम पेज पर अपने आप दिखता है: यह सबसे नए रिकॉर्ड की `updated` तारीख या `content/updates.json` की सबसे नई तारीख होती है। हाथ से बदलने की ज़रूरत नहीं।
- **क्या नया है?** (`content/updates.json`): हर एंट्री में `date`, `hi`, `en`, ज़रूरत हो तो `dhi`/`den` (एक लाइन विवरण), `url` (पूरी जानकारी वाला पेज), और चाहें तो `expires`। `expires` न हो तो एंट्री 180 दिन बाद अपने आप हट जाती है। सबसे नई सबसे ऊपर; होम पेज पर ताज़ा 3 दिखती हैं।
- **तारीख निकलने पर अपने आप हटना:** किसी योजना/दस्तावेज़ के JSON में `"valid_until": "YYYY-MM-DD"` डालें। उस तारीख के बाद अगली build में वह पेज, खोज, sitemap और राज्य-पेज से अपने आप हट जाता है (build में `EXPIRED (hidden)` दिखता है)।
- **दोबारा जाँच:** जिस पेज का `last_verified` 180 दिन से पुराना है, उस पर पाठकों को "6 महीने से पुरानी जाँच" वाली सूचना दिखती है और build में `REVIEW DUE` लिखा आता है।
- यह सब build की तारीख से जाँचा जाता है (Cloudflare पर deploy के दिन की तारीख)। जाँच के लिए कोई और तारीख देनी हो तो `BUILD_DATE=YYYY-MM-DD python3 build.py`।
