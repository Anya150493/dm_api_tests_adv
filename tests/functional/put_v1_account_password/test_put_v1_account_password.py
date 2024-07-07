import allure

from checkers.http_checkers import check_status_code_http

@allure.suite("Тесты на проверку метода PUT v1/account/password")
@allure.sub_suite("Позитивные тесты")
class TestsPutV1AccountPassword:
    def test_put_v1_account_password(
            self,
            account_helper,
            prepare_user
            ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        new_password = "987654321"
        with check_status_code_http(400, 'Validation failed'):
            account_helper.register_new_user(login=login, password=password, email=email)
            account_helper.user_login(login=login, password=password)
            account_helper.change_password(login=login, email=email, old_password=password, new_password=new_password)
            account_helper.user_login(login=login, password=new_password)
