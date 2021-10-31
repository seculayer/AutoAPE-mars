# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
import http.client
import json
import random
from typing import List

from mars.common.Constants import Constants


class RandomRecommender(object):
    def __init__(self):
        self.http_client: http.client.HTTPConnection = http.client.HTTPConnection(
            Constants.MRMS_SVC, Constants.MRMS_REST_PORT)

        self.ALGORITHM_POOL = ["KDNN", "KCNN"]
        self.algorithm_info = self.get_algorithm_info()
        print(self.algorithm_info)

    def get_algorithm_info(self):
        self.http_client.request("GET", "/mrms/get_algorithm_info")
        response = self.http_client.getresponse()
        str_data = response.read()
        print(str_data)
        data = json.loads(str_data)
        response.close()
        result_dict = dict()
        for algorithm in data:
            result_dict[algorithm.get("alg_cls")] = algorithm.get("alg_id")
        return result_dict

    def recommend(self, dprs_list):
        result = list()

        for idx, dprs_data in enumerate(dprs_list):
            alg_cls = random.choice(self.ALGORITHM_POOL)
            alg_id = self.algorithm_info.get(alg_cls)

            result.append(
                {"alg_cls": alg_cls, "alg_id": alg_id, "metadata_json": {}, "alg_json": {}, "alg_type": "1"}
            )

        return result


if __name__ == '__main__':
    RandomRecommender()
