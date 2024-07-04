from checkers.post_v1_account import PostV1Account


def test_post_v1_account(
        account_helper,
        prepare_user

):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1Account.check_response_values(response)



