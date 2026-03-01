import api

login = api.login('zana@gmail.com','zana@gmail.com')
print('login', login)
user = login.get('user')
uid = user.get('id')
print('user id', uid)
print('files', api.get_user_files(uid))
