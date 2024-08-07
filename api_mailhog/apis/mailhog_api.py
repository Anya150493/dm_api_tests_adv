import allure
import requests

from restclient.client import RestClient


class MailhogApi(RestClient):

    @allure.step("Получить все письма")
    def get_api_v2_messages(
            self,
            limit=50
    ):
        """
        get Users emails
        :return:
        """
        params = {
            'limit': limit
        }
        response = self.get(
            path=f'/api/v2/messages',
            params=params,
            verify=False
        )
        return response
