# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.

import requests as rq
import json

from mars.common.Common import Common
from mars.common.Constants import Constants
from mars.manager.SFTPClientManager import SFTPClientManager
from mars.recommender.RandomRecommender import RandomRecommender


class MARSManager(object):
    # class : DataAnalyzerManager
    def __init__(self, job_id, job_idx):
        self.logger = Common.LOGGER.get_logger()

        self.mrms_sftp_manager: SFTPClientManager = SFTPClientManager(
            "{}:{}".format(Constants.MRMS_SVC, Constants.MRMS_SFTP_PORT), Constants.MRMS_USER, Constants.MRMS_PASSWD)

        self.rest_root_url = f"http://{Constants.MRMS_SVC}:{Constants.MRMS_REST_PORT}"

        self.job_id = job_id
        self.current = 0
        self.logger.info("MARSManager initialized.")

    def load_job_info(self, filename):
        return self.mrms_sftp_manager.load_json_data(filename)

    def recommend(self):
        filename = "{}/DPRS_{}_{}.info".format(Constants.DIR_DIVISION_PATH, self.job_id, self.current)
        if self.mrms_sftp_manager.is_exist(filename):
            job_info = self.load_job_info(filename)
            results = list()
            for dprs_data in job_info:
                results += RandomRecommender().recommend(dprs_data, self.job_id)

            response = rq.post(f"{self.rest_root_url}/mrms/insert_alg_anls_info", json=results)
            self.logger.info(f"insert alg anls info: {response.status_code} {response.reason} {response.text}")

            f = self.mrms_sftp_manager.get_client().open(
                "{}/MARS_{}_{}.info".format(Constants.DIR_DIVISION_PATH, self.job_id, self.current),
                "w"
            )
            f.write(json.dumps(results, indent=2))
            f.close()
            self.current += 1

    def get_terminate(self) -> bool:
        response = rq.get(f"{self.rest_root_url}/mrms/get_proj_sttus_cd?project_id={self.job_id}")
        status = response.text.replace("\n", "")
        if status == Constants.STATUS_PROJECT_COMPLETE or status == Constants.STATUS_PROJECT_ERROR:
            return True
        return False


if __name__ == '__main__':
    dam = MARSManager("ID", "0")
