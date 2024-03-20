# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.

import requests as rq
import random

from mars.common.Constants import Constants
from mars.common.Common import Common


class RandomRecommender(object):
    def __init__(self, project_purpose_cd, project_tag_list):
        self.project_purpose_cd = project_purpose_cd
        self.project_tag_list = project_tag_list
        self.rest_root_url = f"http://{Constants.MRMS_SVC}:{Constants.MRMS_REST_PORT}"

        # list idx(dataset_format) - 0: None(empty), 1: text, 2: image
        # dict key(project_purpose_cd - 1: Classifier, 10: TA
        self.ALGORITHM_POOL = [
            {},
            {
                "1": [
                    "KDNN", "KCNN", "SKLExtraTrees", "SKLRandomForest",
                    "SKLGaussianNB", "SKLDecisionTree",  # "SKLSVC",
                    "XGBoost", "SKLIsolationForest", "LightGBM", "KTMSFeedBackKNN"
                    # "SKLBernoulliNB", "SKLLinearSVC", "SKLKNeighbors", "SKLMLP"
                ],
                "10": [
                    "TFGPRMV2"
                ]
            },
            {
                "1": ["KCNN", "KDNN"]
            },
            {
                "1": [
                    "KDNN", "KCNN", "SKLExtraTrees", "SKLRandomForest",
                    "SKLGaussianNB", "SKLDecisionTree",  # "SKLSVC",
                    "XGBoost", "SKLIsolationForest", "LightGBM", "KTMSFeedBackKNN"
                    # "SKLBernoulliNB", "SKLLinearSVC", "SKLKNeighbors", "SKLMLP"
                ],
                "10": [
                    "TFGPRMV2"
                ]
            }
        ]
        self.SPECIFIC_ALGORITHM_POOL = {
            "dga": "XGBoost",
            "packet": "SKLIsolationForest",
            "meta": "LightGBM"
        }
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

    def get_algorithm_info(self):
        return {
            "KDNN": {"alg_id": "20000000000000001", "alg_type": "1"},
            "KCNN": {"alg_id": "20000000000000002", "alg_type": "1"},
            "KTMSFeedBackKNN": {"alg_id": "20000000000000008", "alg_type": "1"},
            "SKLExtraTrees": {"alg_id": "50000000000000001", "alg_type": "1"},
            "SKLRandomForest": {"alg_id": "50000000000000002", "alg_type": "1"},
            "SKLBernoulliNB": {"alg_id": "50000000000000003", "alg_type": "1"},
            "SKLGaussianNB": {"alg_id": "50000000000000004", "alg_type": "1"},
            "SKLKNeighbors": {"alg_id": "50000000000000005", "alg_type": "1"},
            "SKLMLP": {"alg_id": "50000000000000006", "alg_type": "1"},
            "SKLLinearSVC": {"alg_id": "50000000000000007", "alg_type": "1"},
            "SKLSVC": {"alg_id": "50000000000000009", "alg_type": "1"},
            "SKLDecisionTree": {"alg_id": "50000000000000010", "alg_type": "1"},
            "TFGPRMV2": {"alg_id": "10000000000000001", "alg_type": "10"},
            "XGBoost": {"alg_id": "10000000000000002", "alg_type": "1"},
            "SKLIsolationForest": {"alg_id": "50000000000000015", "alg_type": "1"},
            "LightGBM": {"alg_id": "10000000000000003", "alg_type": "1"}
        }

    def get_uuid(self):
        response = rq.get(f"{self.rest_root_url}/mrms/get_uuid")
        return response.text.replace("\n", "")

    def recommend(self, dprs_dict, job_id, dataset_format):
        result = list()
        alg_pool: list = self.ALGORITHM_POOL[int(dataset_format)][self.project_purpose_cd]
        # Scikit Learn 일 경우 multi class 지원 x
        if dprs_dict["data_analysis_json"][0]["statistic"].__contains__("unique"):
            label_kind_cnt = dprs_dict["data_analysis_json"][0]["statistic"]["unique"]["unique_count"]

            if label_kind_cnt > 2:
                remove_val_list = list()
                for alg in alg_pool:
                    if alg[:3] == "SKL":
                        remove_val_list.append(alg)
                for alg in remove_val_list:
                    alg_pool.remove(alg)

        Common.LOGGER.getLogger().info(f"tag list : {self.project_tag_list}")

        is_specific_case = None
        for tag in self.project_tag_list:
            if "dga" in tag.lower():
                is_specific_case = self.SPECIFIC_ALGORITHM_POOL["dga"]
                break
            elif "packet" in tag.lower():
                is_specific_case = self.SPECIFIC_ALGORITHM_POOL["packet"]
                break
            elif "meta" in tag.lower():
                is_specific_case = self.SPECIFIC_ALGORITHM_POOL["meta"]
                break

        Common.LOGGER.getLogger().info(f"is_specific_case : {is_specific_case}")
        for idx in range(random.randint(Constants.RCMD_MIN_COUNT, Constants.RCMD_MAX_COUNT)):
            if is_specific_case is not None:
                alg_cls = is_specific_case
                is_specific_case = None
            else:
                alg_cls = random.choice(alg_pool)
            try:
                alg_id = self.algorithm_info.get(alg_cls).get("alg_id")
                alg_type = self.algorithm_info.get(alg_cls).get("alg_type")
            except Exception as e:
                Common.LOGGER.getLogger().error(f"alg_cls: {alg_cls}")
                raise e

            result.append(
                {"alg_cls": alg_cls, "alg_id": alg_id, "project_id": job_id,
                 "alg_anal_id": self.get_uuid(), "dp_analysis_id": dprs_dict.get("dp_analysis_id"),
                 "metadata_json": {}, "alg_json": {}, "alg_type": alg_type,
                 "dataset_format": dataset_format}
            )

        return result


if __name__ == '__main__':
    RandomRecommender()
