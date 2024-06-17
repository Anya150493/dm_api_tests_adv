import requests

from restclient.client import RestClient
from restclient.configuration import Configuration


class AccountApi(RestClient):

    def __init__(
            self,
            configuration: Configuration
    ):
        super().__init__(configuration)
        self.login_api = None
        self.account_api = None

    def post_v1_account(
            self,
            json_data
    ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=json_data
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain'
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        return response

    def put_v1_account_email(
            self,
            json_data
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = requests.put(
            url=f'{self.host}/v1/account/email',
            json=json_data
        )
        return response


