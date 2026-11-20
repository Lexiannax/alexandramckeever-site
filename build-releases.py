# Rebuilds the "Releases" section of index.html from releases.json (newest first).
# To add a release: put its cover in images/<slug>.jpg (python add-release.py <slug> does this), then run:  python build-releases.py
import json, html, datetime, re

SHOW_FIRST = 12          # how many show before "Show all"
rel = json.load(open('releases.json', encoding='utf-8'))
rel.sort(key=lambda r: r['date'], reverse=True)
NL = chr(10)

def month(d):
    return datetime.date.fromisoformat(d).strftime('%B %Y')

cards = []
for i, r in enumerate(rel):
    t = html.escape(r['title'])
    cls = ' class="more"' if i >= SHOW_FIRST else ''
    url = 'https://distrokid.com/hyperfollow/alexandramckeever/' + r['slug']
    cards.append(f'''          <li{cls}>
            <a href="{url}"><img src="images/{r['slug']}.jpg" alt="Cover art for {t} by Alexandra McKeever" width="600" height="600" loading="lazy" /></a>
            <h3>{t}</h3>
            <p class="meta">Single &middot; {month(r['date'])}</p>
            <a class="btn small" href="{url}">Listen</a>
          </li>''')

n = len(rel)
more = ''
if n > SHOW_FIRST:
    more = f'''        <p class="more-wrap"><button type="button" class="btn" id="show-all" aria-expanded="false" aria-controls="releases-list">Show all {n} releases</button></p>
        <noscript><style>.releases .more{{display:block !important}}</style></noscript>
        <script>(function(){{var b=document.getElementById("show-all"),l=document.getElementById("releases-list");if(!b)return;b.addEventListener("click",function(){{var c=l.classList.toggle("collapsed");b.textContent=c?"Show all {n} releases":"Show fewer";b.setAttribute("aria-expanded",String(!c));}});}})();</script>
'''
collapsed = ' collapsed' if more else ''
block = f'''<!-- releases:start -->
      <section id="releases" aria-labelledby="rel-h">
        <h2 id="rel-h">Releases</h2>
        <p class="lede">Pick your favorite service. Each button opens a page with every place to listen.</p>
        <ul class="releases{collapsed}" id="releases-list">
{NL.join(cards)}
        </ul>
{more}      </section>
      <!-- releases:end -->'''

s = open('index.html', encoding='utf-8', newline='').read()
assert '<!-- releases:start -->' in s
s = re.sub(r'<!-- releases:start -->.*?<!-- releases:end -->', lambda m: block, s, flags=re.S)
open('index.html', 'w', encoding='utf-8', newline='').write(s)
print('index.html updated with', n, 'releases;', max(0, n - SHOW_FIRST), 'hidden until "Show all"')
