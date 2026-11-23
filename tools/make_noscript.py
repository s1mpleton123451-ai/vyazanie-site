#!/usr/bin/env python3
"""Пересобирает статичный список вещей для людей и роботов без JavaScript.
Запуск после любого изменения CONFIG.items в index.html:  python3 tools/make_noscript.py"""
import re, html, pathlib
p = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
s = p.read_text(encoding='utf-8')
cfg = s[s.index('const CONFIG'):s.index('/* ====', s.index('const CONFIG'))]
items = re.findall(r"name: '([^']+)',\s+img: '([^']+)',\s+price: '([^']*)',\s+text: '([^']+)'", cfg)
tg = re.search(r"telegram: '([^']+)'", cfg).group(1)
li = ''.join(f'<li><img src="img/{i}" alt="{html.escape(n)}" width="150" height="200" loading="lazy"> <b>{html.escape(n)}</b>, {html.escape(pr or "цену подскажет Александра")}. {html.escape(t)}</li>' for n, i, pr, t in items)
block = f'<!--NOSCRIPT--><section style="padding:90px 20px 20px;max-width:760px;margin:auto"><p>Для работы каталога нужен JavaScript. Вещи ручной работы Александры:</p><ul>{li}</ul><p>Написать Александре: <a href="https://t.me/{tg}">Telegram @{tg}</a>.</p></section><!--/NOSCRIPT-->'
s = re.sub(r'<!--NOSCRIPT-->.*?<!--/NOSCRIPT-->', lambda m: block, s, flags=re.S)
p.write_text(s, encoding='utf-8')
print('вещей в списке:', len(items))
