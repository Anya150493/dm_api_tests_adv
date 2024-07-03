from datetime import datetime

import pytest
from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to,
)
from checkers.http_checkers import (
    check_status_code_http
)


@pytest.mark.parametrize(
    'login, email, password,expected_status_code, error_message',
    [
        ('medvedeva', 'medvedeva@mail.ru', '111', 400, 'Validation failed'),
        ('medvedeva', 'medvedeva.mail.ru', '12233332', 400, 'Validation failed'),
        ('123###', 'medvedeva@mail.ru', '12233332', 400, 'Validation failed')
    ]
)
def test_post_v1_account(
        account_helper,
        prepare_user,
        login,
        email,
        password,
        expected_status_code,
        error_message

):
    # login = prepare_user.login
    # email = prepare_user.email
    # password = prepare_user.password
    with check_status_code_http(400, 'Validation failed'):
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, validate_response=True)

        assert_that(
            response, all_of(
                has_property('resource', has_property('login', starts_with("medvedeva"))),
                has_property('resource', has_property('registration', instance_of(datetime))),
                has_property(
                    'resource', has_properties(
                        {
                            'rating': has_properties(
                                {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0)
                                }
                            )
                        }
                    )
                )
            )
        )
        print(response)
