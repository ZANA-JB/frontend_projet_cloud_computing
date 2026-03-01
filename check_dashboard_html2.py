import requests
import re

s = requests.Session()
# login first
s.post('http://127.0.0.1:5000/login', data={'email':'zana@gmail.com','password':'zana@gmail.com'})
resp = s.get('http://127.0.0.1:5000/dashboard')
html = resp.text
print('public link present?', 'Fichiers publics' in html)
print('Favoris' in html, 'Corbeille' in html)
print('public section heading present?', '<h3 class="text-2xl font-bold' in html and 'Fichiers publics' in html)

nav = re.search(r'<nav.*?</nav>', html, flags=re.S)
print('\n---- sidebar nav ----')
print(nav.group(0) if nav else 'no nav')
print('\n--- lines containing phrase ---')
for line in html.splitlines():
    if 'Fichiers publics' in line:
        print(line)
