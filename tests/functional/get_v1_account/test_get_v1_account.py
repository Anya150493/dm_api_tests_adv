from datetime import datetime

import allure
from hamcrest import (
    all_of,
    has_property,
    instance_of,
    starts_with,
    has_properties,
    equal_to,
)

from checkers.get_v1_aacount import GetV1Account
from checkers.http_checkers import check_status_code_http
from assertpy import assert_that, soft_assertions

from dm_api_account.models.user_details_envelope import UserRole


@allure.suite("Тесты на проверку метода GET v1/account/auth")
@allure.sub_suite("Позитивные тесты")
class TestsGetV1AccountAuth:
    def test_get_v1_account_auth(
            self,
            auth_account_helper
    ):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account()
        GetV1Account.get_check_response_values(response)




@allure.suite("Тесты на проверку метода GET v1/account/auth")
@allure.sub_suite("Позитивные тесты")
class TestsGetV1AccountNoAuth:
    def test_get_v1_account_no_auth(
            self,
            account_helper
    ):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.dm_account_api.account_api.get_v1_account()
