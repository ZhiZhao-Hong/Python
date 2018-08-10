# -*- coding:utf-8 -*-
# urllib
# requests
import requests

class HTTP():

    @ staticmethod
    def get(url, params=None, return_json=True, **kwargs):
        print (url)
        res = requests.get(url, params, **kwargs)

        # if res.status_code == 200:
        #     if return_json is True:
        #         return res.json()
        #     else:
        #         return res.text
        # else:
        #     if return_json is True:
        #         return {}
        #     else:
        #         return ''

        # 三元表达式简写
        if res.status_code != 200:
            return {} if return_json else ''
        else:
            return res.json() if return_json else res.text

        #