#!/usr/bin/env python3
"""Собирает из content/site.json статичные части index.html: заголовок вкладки, превью для мессенджеров,
список вещей без JavaScript и разметку товаров для поисковиков (JSON-LD).
Запускается сам на GitHub при каждом сохранении в админке (.github/workflows/pages.yml).
Вручную: python3 tools/make_noscript.py"""
import re, html, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
p = root / 'index.html'
s = p.read_text(encoding='utf-8')
d = json.loads((root / 'content' / 'site.json').read_text(encoding='utf-8'))
brand, tg = d.get('brand') or 'Вязаные вещи', d.get('telegram') or ''
items = [it for it in d.get('items', []) if it.get('name') and it.get('photo')]
E = html.escape
src = lambda f: str(f).lstrip('/')
def price(it):
    if it.get('status') == 'sold': return 'продано'
    return it.get('price') or 'цену подскажет Александра'
li = ''.join(f'<li><img src="{E(src(it["photo"]))}" alt="{E(it["name"])}" width="150" height="200" loading="lazy"> <b>{E(it["name"])}</b>, {E(price(it))}. {E(it.get("text", ""))}</li>' for it in items)
block = f'<!--NOSCRIPT--><section style="padding:90px 20px 20px;max-width:760px;margin:auto"><p>Для работы каталога нужен JavaScript. Вещи ручной работы Александры:</p><ul>{li}</ul><p>Написать Александре: <a href="https://t.me/{E(tg)}">Telegram @{E(tg)}</a>.</p></section><!--/NOSCRIPT-->'
s = re.sub(r'<!--NOSCRIPT-->.*?<!--/NOSCRIPT-->', lambda m: block, s, flags=re.S)
base = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1)
def product(it):
    o = {'@type': 'Product', 'name': it['name'], 'description': it.get('text', ''), 'image': base + src(it['photo'])}
    pr = it.get('price', '')
    if re.fullmatch(r'\d[\d\s]*₽', pr) and it.get('status') != 'sold':
        o['offers'] = {'@type': 'Offer', 'priceCurrency': 'RUB', 'price': re.sub(r'\D', '', pr), 'availability': 'https://schema.org/' + ('PreOrder' if it.get('status') == 'order' else 'InStock')}
    return o
ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': brand, 'itemListElement': [{'@type': 'ListItem', 'position': k + 1, 'item': product(it)} for k, it in enumerate(items)]}
s = re.sub(r'<!--LD-->.*?<!--/LD-->', lambda m: '<!--LD--><script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace('</', '<\\/') + '</script><!--/LD-->', s, flags=re.S)
s = re.sub(r'<title>[^<]*?( — [^<]*)</title>', lambda m: f'<title>{E(brand)}{m.group(1)}</title>', s, count=1)
s = re.sub(r'(<meta property="og:title" content=")[^"]*?( — [^"]*")', lambda m: m.group(1) + E(brand) + m.group(2), s, count=1)
p.write_text(s, encoding='utf-8')
print('вещей в списке:', len(items))
