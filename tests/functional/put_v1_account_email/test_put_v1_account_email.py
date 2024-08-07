import allure


@allure.suite("Тесты на проверку метода PUT v1/account/email")
@allure.sub_suite("Позитивные тесты")
class TestsPutV1AccountEmail:
    def test_put_v1_account_email(
            self,
            account_helper,
            prepare_user
            ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)
        response=account_helper.change_email(login=login, password=password, email=email)
        print(response.resource.login)
        account_helper.user_login(login=login, password=password)
