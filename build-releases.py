# Rebuilds the "Releases" section of index.html from releases.json (newest first).
# To add a release: put its cover in images/<slug>.jpg, add a line to releases.json, then run:  python build-releases.py
import json, html, datetime, re
rel = json.load(open('releases.json', encoding='utf-8'))
rel.sort(key=lambda r: r['date'], reverse=True)
def month(d): return datetime.date.fromisoformat(d).strftime('%B %Y')
cards = []
for r in rel:
    t = html.escape(r['title'])
    cards.append(
      '          <li>\n'
      '            <a href="https://distrokid.com/hyperfollow/alexandramckeever/%s"><img src="images/%s.jpg" alt="Cover art for %s by Alexandra McKeever" width="600" height="600" loading="lazy" /></a>\n'
      '            <h3>%s</h3>\n'
      '            <p class="meta">Single &middot; %s</p>\n'
      '            <a class="btn small" href="https://distrokid.com/hyperfollow/alexandramckeever/%s">Listen</a>\n'
      '          </li>' % (r['slug'], r['slug'], t, t, month(r['date']), r['slug']))
block = ('<!-- releases:start -->\n'
         '      <section id="releases" aria-labelledby="rel-h">\n'
         '        <h2 id="rel-h">Releases</h2>\n'
         '        <p class="lede">Pick your favorite service. Each button opens a page with every place to listen.</p>\n'
         '        <ul class="releases">\n' + '\n'.join(cards) + '\n        </ul>\n'
         '      </section>\n'
         '      <!-- releases:end -->')
s = open('index.html', encoding='utf-8', newline='').read()
if '<!-- releases:start -->' in s:
    s = re.sub(r'<!-- releases:start -->.*?<!-- releases:end -->', lambda m: block, s, flags=re.S)
else:
    anchor = '      <section id="art"'
    assert s.count(anchor) == 1
    s = s.replace(anchor, '      ' + block + '\n\n' + anchor)
    s = s.replace('      <a href="#art">Art</a>', '      <a href="#releases">Releases</a>\n      <a href="#art">Art</a>')
    css = ('    .releases { display:grid; gap:1.6rem; grid-template-columns:repeat(auto-fill,minmax(min(100%,13rem),1fr)); list-style:none; padding:0; margin:1.2rem 0 0; }\n'
           '    .releases img { width:100%; height:auto; aspect-ratio:1/1; object-fit:cover; display:block; border-radius:8px; border:1px solid var(--line); background:#fff; }\n'
           '    .releases h3 { font-family:"Cormorant Garamond",Georgia,serif; font-size:1.45rem; line-height:1.15; margin:.6rem 0 0; }\n'
           '    .releases .meta { margin:.1rem 0 0; color:var(--muted); font-size:.92rem; }\n'
           '    .btn.small { padding:.45rem 1.1rem; font-size:.95rem; margin-top:.6rem; }\n')
    marker = '    .art-empty {'
    assert s.count(marker) == 1
    s = s.replace(marker, css + marker)
open('index.html', 'w', encoding='utf-8', newline='').write(s)
print('index.html updated with', len(rel), 'releases')
