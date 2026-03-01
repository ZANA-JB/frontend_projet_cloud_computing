import requests

URL='http://127.0.0.1:5000'
session = requests.Session()

# fetch login page
resp = session.get(URL + '/login')
print('login page', resp.status_code)

# perform login
payload = {'email': 'zana@gmail.com', 'password': 'zana@gmail.com'}
resp2 = session.post(URL + '/login', data=payload, allow_redirects=True)
print('login post', resp2.status_code, resp2.url)
print('cookies after login', session.cookies.get_dict())

# prepare file
with open('temp_test_upload.txt', 'w', encoding='utf-8') as f:
    f.write('hello from simulate_upload')

files = {'file': open('temp_test_upload.txt', 'rb')}
data = {
    'name': 'page-upload',
    'status': 'private',
    'user_id': '54787502-fa92-44f0-b46d-cde1a08768e9'
}

resp3 = session.post(URL + '/upload', files=files, data=data, allow_redirects=True)
print('upload status', resp3.status_code)
print('upload response headers', resp3.headers)

# look for flash messages in the returned HTML by scanning for the
# stylized divs used by base.html (bg-red or bg-green)
from bs4 import BeautifulSoup
soup = BeautifulSoup(resp3.text, 'html.parser')
flashes = soup.select('div.mb-2')
if flashes:
    print('flash messages:')
    for f in flashes:
        print('   ', f.get_text(strip=True))
else:
    print('no flash messages found')

# optionally dump entire body for debug
#print('full body:')
#print(resp3.text)

# list files via API to see if new file exists
resp4 = session.get(URL + '/dashboard')
print('dashboard page length', len(resp4.text))
