"""
API CONNECTION FOR IMPORTING WRAPPER
"""
import json
import logging
import requests
from utils import envs


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


class APIConnection:
    """
    Api Connection
    """

    def __init__(self):
        self.api_url = envs.API_URL

        self.token = None
        self.headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        }
        self.request_jwt()

    def request_jwt(self):
        """
        Request JWT token.
        """
        logging.info("Requesting JWT..")

        api_url = f"{self.api_url}api/token/"
        data = {
            "username": envs.SCRIPT_USER,
            "password": envs.SCRIPT_PASSWORD,
        }

        res = requests.post(api_url, data=json.dumps(data), headers=self.headers)

        if res.status_code == 200:
            data = res.json()
            self.token = data["access"]
            self.headers["Authorization"] = f"Bearer {self.token}"
        else:
            logging.error(
                f"Failed to obtain JWT. Status code: {res.status_code}, Message: {res.text}"
            )

    def post_data(self, item, api):
        """
        post data
        :param item: items to be posted in json format
        :param api: path of endpoint
        """
        api_url = f"{self.api_url}{api}"

        try:
            res = requests.post(
                api_url, data=json.dumps(item), headers=self.headers, timeout=60
            )

            if res.status_code == 401:
                self.request_jwt()
                self.post_data(item, api)

            elif res.status_code in [200, 201]:
                logging.info(f"{res.status_code} - data posted successfully")
                return res.status_code

            else:
                logging.error(f"{res.status_code} - {res.json()}- unable to post data")
                return res.status_code

        except Exception as err:
            logging.error(err)
            return 500

    def upload_video(self, api, file):
        """
        post data
        :param item: items to be posted in json format
        :param api: path of endpoint
        """
        api_url = f"{self.api_url}{api}"
        self.headers["Content-Type"] = "multipart/form-data"

        try:
            res = requests.post(api_url, files=file, headers=self.headers, timeout=60)

            if res.status_code == 401:
                self.request_jwt()
                self.post_data(api, file)

            elif res.status_code in [200, 201]:
                logging.info(f"{res.status_code} - video uploaded successfully")
                return res.status_code

            else:
                logging.error(
                    f"{res.status_code} - {res.json()}- unable to upload video"
                )
                return res.status_code

        except Exception as err:
            logging.error(err)
            return 500
