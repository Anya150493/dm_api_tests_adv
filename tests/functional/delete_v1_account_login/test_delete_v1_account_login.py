import allure


@allure.suite("Тесты на проверку метода DELETE v1/account/login")
@allure.sub_suite("Позитивные тесты")
class TestsDeleteV1AccountLogin:
    def test_delete_v1_account_login(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password)
        token = response.headers['X-Dm-Auth-Token']

        account_helper.logout_user(
            headers={
                "X-Dm-Auth-Token": token
            }
            )
