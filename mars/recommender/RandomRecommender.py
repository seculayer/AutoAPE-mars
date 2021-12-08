# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.

import requests as rq
import random

from mars.common.Constants import Constants


class RandomRecommender(object):
    def __init__(self):
        self.rest_root_url = f"http://{Constants.MRMS_SVC}:{Constants.MRMS_REST_PORT}"

        self.ALGORITHM_POOL = [
            "KDNN", "KCNN", "SKLExtraTrees", "SKLRandomForest", "SKLBernoulliNB",
            "SKLGaussianNB", "SKLKNeighbors", "SKLMLP", "SKLLinearSVC", "SKLSVC",
            "SKLDecisionTree"
                               ]
        self.algorithm_info = self.get_algorithm_info()

    # def get_algorithm_info(self):
    #     self.http_client.request("GET", "/mrms/get_algorithm_info")
    #     response = self.http_client.getresponse()
    #     str_data = response.read()
    #     print(str_data)
    #     data = json.loads(str_data)
    #     response.close()
    #     result_dict = dict()
    #     for algorithm in data:
    #         result_dict[algorithm.get("alg_cls")] = algorithm.get("alg_id")
    #     return result_dict

    @staticmethod
    def get_algorithm_info():
        return {
            "KDNN": "20000000000000001", "KCNN": "20000000000000002",
            "SKLExtraTrees": "50000000000000001", "SKLRandomForest": "50000000000000002",
            "SKLBernoulliNB": "50000000000000003", "SKLGaussianNB": "50000000000000004",
            "SKLKNeighbors": "50000000000000005", "SKLMLP": "50000000000000006",
            "SKLLinearSVC": "50000000000000007", "SKLSVC": "50000000000000009",
            "SKLDecisionTree": "50000000000000010"
        }

    def get_uuid(self):
        response = rq.get(f"{self.rest_root_url}/mrms/get_uuid")
        return response.text.replace("\n", "")

    def recommend(self, dprs_dict, job_id):
        result = list()

        for idx in range(random.randint(Constants.RCMD_MIN_COUNT, Constants.RCMD_MAX_COUNT)):
            alg_cls = random.choice(self.ALGORITHM_POOL)
            alg_id = self.algorithm_info.get(alg_cls)

            result.append(
                {"alg_cls": alg_cls, "alg_id": alg_id, "project_id": job_id,
                 "alg_anal_id": self.get_uuid(), "dp_analysis_id": dprs_dict.get("dp_analysis_id"),
                 "metadata_json": {}, "alg_json": {}, "alg_type": "1"}
            )

        return result


if __name__ == '__main__':
    RandomRecommender()
