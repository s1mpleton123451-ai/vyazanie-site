#!/usr/bin/env python3
"""Подключает свой домен к сайту: python3 tools/set_domain.py odnatakaya.ru
Пишет файл CNAME и заменяет адрес сайта в index.html и sitemap.xml.
Сначала купите домен и в его настройках (DNS) добавьте 4 записи A: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
и запись CNAME для www на s1mpleton123451-ai.github.io. Потом: commit и push, в настройках репозитория Pages включить Enforce HTTPS."""
import sys, pathlib
OLD = 'https://s1mpleton123451-ai.github.io/vyazanie-site/'
root = pathlib.Path(__file__).resolve().parent.parent
if len(sys.argv) != 2 or '.' not in sys.argv[1]:
    sys.exit(__doc__)
d = sys.argv[1].strip().lower().removeprefix('https://').removeprefix('http://').strip('/')
new = f'https://{d}/'
(root / 'CNAME').write_text(d + '\n')
for f in ('index.html', 'sitemap.xml', '404.html', 'robots.txt'):
    p = root / f; t = p.read_text(encoding='utf-8'); p.write_text(t.replace(OLD, new), encoding='utf-8')
print('готово:', new)
