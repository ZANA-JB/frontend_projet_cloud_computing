from app import app
import io

# create test client
with app.test_client() as client:
    # first login via the form
    resp = client.post('/login', data={'email': 'zana@gmail.com', 'password': 'zana@gmail.com'}, follow_redirects=True)
    print('login status', resp.status_code)
    # check session cookie
    print('cookies', resp.headers.get('Set-Cookie'))

    data = {
        'name': 'page-upload-test',
        'status': 'private',
        'user_id': '54787502-fa92-44f0-b46d-cde1a08768e9'
    }
    # create a file-like object and merge into form data
    data['file'] = (io.BytesIO(b'hello'), 'mytest.txt')
    resp2 = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    print('upload status', resp2.status_code)
    # inspect flashes in the HTML reply
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp2.data, 'html.parser')
    messages = soup.select('div.mb-2')
    print('flashed messages:')
    for m in messages:
        print('   ', m.get_text(strip=True))
    print('body length', len(resp2.data))

    # read debug log if exists
    import os
    logpath = 'upload_debug.log'
    if os.path.exists(logpath):
        print('log file content:')
        print(open(logpath).read())
    else:
        print('no log file created')
