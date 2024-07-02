from datetime import datetime

from checkers.http_checkers import check_status_code_http
from assertpy import assert_that, soft_assertions

from dm_api_account.models.user_details_envelope import UserRole


def test_get_v1_account_auth(
        auth_account_helper
):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    with soft_assertions():
        assert_that(response.resource.login).is_equal_to("medvedeva_26_06_2024_15_48_59")
        assert_that(response.resource.online).is_instance_of(datetime)
        assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)



def test_get_v1_account_no_auth(
        account_helper
):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account()
