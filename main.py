import vk_api
from vk_auth import VKAuth

code = ""
redirect_url = 'vk.com/blank.html'
app_id = ""
secret = ""

login = ""
password = ""

if __name__ == "__main__":
    auth = VKAuth(app_id, "friends", login, password)
    auth.get_access_token()
