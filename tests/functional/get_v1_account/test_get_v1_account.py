from datetime import datetime

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


def test_get_v1_account_auth(
        auth_account_helper
):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    GetV1Account.get_check_response_values(response)




def test_get_v1_account_no_auth(
        account_helper
):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account()
