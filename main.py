import vk_api
from vk_auth import VKAuth

code = 'fda5414ed49c16806f'
redirect_url = 'vk.com/blank.html'
app_id = 51861517
secret = 'PY5maAdTlWsMMCrtOF28'

login = "89030759420"
password = "tyX7~Lp3+"

if __name__ == "__main__":
    auth = VKAuth(app_id, "friends", login, password)
    auth.get_access_token()
