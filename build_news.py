#!/usr/bin/env python3
"""Build news.json for Dispatch from feeds.txt (Section|Lang|Source|URL)."""
import json, re, html, time, subprocess, sys, calendar
import feedparser
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
PER_SOURCE = 8
MAX_AGE_DAYS = {"default": 3, "Marketing": 10, "Balkans": 7}
now = time.time()

def fetch(url):
    r = subprocess.run(["curl", "-sL", "--compressed", "-m", "20", "-A", UA,
                        "-H", "Accept: application/rss+xml, application/xml, text/xml, */*", url],
                       capture_output=True)
    return r.stdout

def clean(s, n=240):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = re.sub(r"\s+", " ", s).strip()
    return (s[:n].rsplit(" ", 1)[0] + "…") if len(s) > n else s

items, report = [], []
for line in open(sys.argv[1] if len(sys.argv) > 1 else "feeds.txt", encoding="utf-8"):
    if not line.strip() or line.startswith("#"): continue
    desk, lang, src, url = line.rstrip("\n").split("|", 3)
    gnews = "news.google.com" in url
    try:
        f = feedparser.parse(fetch(url))
    except Exception as e:
        report.append(f"FAIL {src} {lang}: {e}"); continue
    kept = 0
    for pos, e in enumerate(f.entries):
        t = e.get("published_parsed") or e.get("updated_parsed")
        ts = calendar.timegm(t) if t else None
        if ts and now - ts > 86400 * MAX_AGE_DAYS.get(desk, MAX_AGE_DAYS["default"]): continue
        title = clean(e.get("title", ""), 200)
        if gnews: title = re.sub(r"\s+-\s+[^-]+$", "", title)
        if not title or not e.get("link"): continue
        summ = "" if gnews else clean(e.get("summary", ""))
        if summ.lower().startswith(title.lower()[:40]): summ = ""
        items.append({"d": desk, "l": lang, "src": src, "t": title, "p": summ,
                      "u": e.get("link"), "ts": ts, "pos": pos})
        kept += 1
        if kept >= PER_SOURCE: break
    if kept == 0:  # quiet source: keep its two latest items anyway
        for pos, e in enumerate(f.entries[:2]):
            t = e.get("published_parsed") or e.get("updated_parsed")
            title = clean(e.get("title", ""), 200)
            if gnews: title = re.sub(r"\s+-\s+[^-]+$", "", title)
            if not title or not e.get("link"): continue
            items.append({"d": desk, "l": lang, "src": src, "t": title,
                          "p": "" if gnews else clean(e.get("summary", "")),
                          "u": e.get("link"), "ts": calendar.timegm(t) if t else None, "pos": pos})
            kept += 1
    report.append(f"{'OK  ' if kept else 'NONE'} {kept:2d} {desk} {lang} {src}")

# de-duplicate identical titles
seen, out = set(), []
for it in items:
    k = it["t"].lower()
    if k in seen: continue
    seen.add(k); out.append(it)
json.dump({"generated": int(now), "items": out}, open("news.json", "w", encoding="utf-8"), ensure_ascii=False)
print("\n".join(report)); print(f"TOTAL {len(out)} items")
