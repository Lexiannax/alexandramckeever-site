# Adds a release from its DistroKid HyperFollow page:  python add-release.py <slug> [<slug> ...]
# Confirms the artist is Alexandra McKeever, fetches the cover art (resized, no hidden data), and updates releases.json.
import re, sys, json, html, io, os, datetime, urllib.request
from PIL import Image
UA = {'User-Agent': 'Mozilla/5.0'}
def get(url): return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
rel = json.load(open('releases.json', encoding='utf-8')) if os.path.exists('releases.json') else []
have = {r['slug'] for r in rel}
for slug in sys.argv[1:]:
    if slug in have: print(slug, '| already on the site, skipped'); continue
    try:
        h = get('https://distrokid.com/hyperfollow/alexandramckeever/' + slug).decode('utf-8', 'replace')
        og = re.findall(r'<meta[^>]+property="og:title"[^>]*content="([^"]*)"', h)
        full = html.unescape(og[0]) if og else ''
        if not full.endswith(' by Alexandra McKeever'): print(slug, '| NOT confirmed as Alexandra McKeever (og:title: %r), skipped' % full); continue
        title = full[:-len(' by Alexandra McKeever')]
        m = re.search(r'apple\.com(?:&#47;|/)[a-z]{2}(?:&#47;|/)album(?:&#47;|/)[^"\'&/ ]+(?:&#47;|/)(\d+)', h)
        date, art = None, None
        if m:
            j = json.loads(get('https://itunes.apple.com/lookup?id=%s&entity=album&country=us' % m.group(1)))
            r0 = (j.get('results') or [{}])[0]
            if r0.get('artistName') == 'Alexandra McKeever':
                date = r0.get('releaseDate', '')[:10]; art = r0.get('artworkUrl100', '').replace('100x100bb', '600x600bb')
        if not art:
            sp = re.search(r'spotify\.com(?:&#47;|/)album(?:&#47;|/)([A-Za-z0-9]+)', h)
            if sp:
                o = json.loads(get('https://open.spotify.com/oembed?url=https://open.spotify.com/album/' + sp.group(1)))
                art = o.get('thumbnail_url')
        if not art: print(slug, '| no cover art found, skipped'); continue
        im = Image.open(io.BytesIO(get(art))).convert('RGB'); im.thumbnail((600, 600), Image.LANCZOS)
        im.save('images/%s.jpg' % slug, 'JPEG', quality=84, optimize=True, progressive=True)
        rel.append({'slug': slug, 'title': title, 'date': date or datetime.date.today().isoformat()})
        have.add(slug)
        print(slug, '| added: %r, %s%s' % (title, date or 'today', '' if m else ' (cover from Spotify)'))
    except Exception as e:
        print(slug, '| could not be added:', e)
json.dump(rel, open('releases.json', 'w', encoding='utf-8'), indent=1)
