import requests

from config import *
def add(data):
    """

    :param data: post中的内容
    :return:
    """
    requests.post(URL_ADD, json=data)