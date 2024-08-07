import time
from json import loads

import allure

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from services.dm_api_account import DmApiAccount
from services.api_mailhog import MailHogApi
from retrying import retry


def retry_if_result_none(
        result
):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        print(f"Попытка получения токена № {count}")
        while token is None:
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено количество попыток получения активационного токена")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DmApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.user_login(
            login=login,
            password=password
        )
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    @allure.step("Регистрация нового пользователя")
    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login=login,
            password=password,
            email=email
        )

        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не был создан {response.json()}"
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 5, "Время ожидания активации превышено"
        assert token is not None, f"Токен для пользователя {login}, не был получен"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    @allure.step("Аутентификация пользователя")
    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response=False,
            validate_headers=False
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )

        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        if validate_headers:
            assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"
        return response

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login
    ):
        token = None
        time.sleep(3)
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']

            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token

    @allure.step("Смена email")
    def change_email(
            self,
            login: str,
            password: str,
            email: str
    ):
        email = 'medvedeva_test144@mail.ru'

        change_email = ChangeEmail(
            login=login,
            password=password,
            email=email
        )

        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login}, не был получен"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    @allure.step("Разлогин текущим пользователем")
    def logout_user(
            self,
            **kwargs
    ):
        response = self.dm_account_api.login_api.delete_v1_account_login(**kwargs)
        assert response.status_code == 204, f"Текущий пользователь не был разлогинен"

    @allure.step("Разлогин текущим пользователем на всех устройствах")
    def logout_user_all(
            self,
            **kwargs
    ):
        response = self.dm_account_api.login_api.delete_v1_account_login_all(**kwargs)
        assert response.status_code == 204, f"Текущий пользователь не был разлогинен со всех устройств"

    @allure.step("Смена пароля")
    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str,
            validate_response=False
    ):
        token = self.user_login(login=login, password=old_password)
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        self.dm_account_api.account_api.post_v1_account_password(
            reset_password=reset_password,
            validate_response=validate_response,
            # headers={
            #     "x-dm-auth-token": token.headers["x-dm-auth-token"]
            # },
        )
        token = self.get_token(login=login, token_type="reset")
        change_password = ChangePassword(
            login=login,
            token=token,
            old_password=old_password,
            new_password=new_password
        )
        response = self.dm_account_api.account_api.put_v1_account_password(
            change_password=change_password,
            validate_response=validate_response
        )
        return response

    @allure.step("Получение токена активации или сброса пароля")
    @retry(
        stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000
    )
    def get_token(
            self,
            login,
            token_type="activation"
    ):
        """
        Получение токена активации или сброса пароля
        Args:
            login: логин пользователя
            token_type: тип токена (activation или reset)
        Returns:
            токен активации или сброса пароля
        """
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()["items"]:
            user_data = loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            activation_token = user_data.get("ConfirmationLinkUrl")
            reset_token = user_data.get("ConfirmationLinkUri")
            if user_login == login and activation_token and token_type == "activation":
                token = activation_token.split("/")[-1]
            elif user_login == login and reset_token and token_type == "reset":
                token = reset_token.split("/")[-1]

        return token
