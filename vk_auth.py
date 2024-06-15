import requests
from enum_permissions import VKPermissions
from _html_parser import FormParser


# Пропускаем этап с получением кода. Идем сразу за token


class VKAuth:
    id_app: int = None
    permission: str = None
    redirect_url = None

    login_account: str = None
    password_account: str = None

    def __init__(self, id_app: int, permission: str,
                 login: str, password: str,
                 redirect_url: str = "https://oauth.vk.com/blank.html"):
        self.id_app = id_app
        self.redirect_url = redirect_url
        self.set_permission(permission)
        self.login_account = login
        self.password_account = password

    def create_url(self):
        # fuck
        url = ("https://oauth.vk.com/authorize?" +
               f"client_id={self.id_app}" +
               "&display=page&" +
               f"redirect_uri={self.redirect_url}" +
               f"&scope={self.permission}" +
               "response_type=token" +
               "v=5.131")
        return url

    def set_permission(self, permission):
        for e in VKPermissions:
            if e.value is permission:
                self.permission = permission
                break

    def get_url(self):
        return self.create_url()

    def get_access_token(self):
        url = self.create_url()
        response = requests.session().get(url)
        parser = FormParser()
        parser.feed(str(response.content))
        self._log_in(parser)

    def _submit_form(self, parser, *params):
        if parser.method == 'post':
            payload = parser.params
            payload.update(*params)
            try:
                self.response = requests.session().post(parser.url, data=payload)
            except requests.exceptions.RequestException as err:
                print("Error: ", err)
            except requests.exceptions.HTTPError as err:
                print("Error: ", err)
            except requests.exceptions.ConnectionError as err:
                print("Error: ConnectionError\n", err)
            except requests.exceptions.Timeout as err:
                print("Error: Timeout\n", err)
            except:
                print("Unexpecred error occured")
        else:
            self.response = None

    def _log_in(self, _parse_form):
        self._submit_form(_parse_form, {'email': self.login_account, 'pass': self.password_account})

        if not _parse_form:
            raise RuntimeError('No <form> element found. Please, check url address')

        # if wrong email or password
        if 'pass' in _parse_form.params:
            print('Wrong email or password')
            print(_parse_form.params)
            self.login_account = ""
            self.password_account = ""
            return False
        elif 'code' in _parse_form.params:
            self.two_factor_auth = True
        else:
            return True
