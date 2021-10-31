# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
import http.client
import json
from typing import Dict

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

        self.http_client: http.client.HTTPConnection = http.client.HTTPConnection(
            Constants.MRMS_SVC, Constants.MRMS_REST_PORT)

        self.job_id = job_id
        self.logger.info("MARSManager initialized.")

    def load_job_info(self, job_id, idx):
        filename = "{}/DPRS_{}_{}.info".format(Constants.DIR_DIVISION_PATH, job_id, idx)
        return self.mrms_sftp_manager.load_json_data(filename)

    def recommend(self, idx):
        job_info = self.load_job_info(self.job_id, idx)
        results = RandomRecommender().recommend(job_info)

        self.http_client.request("POST", "/mrms/insert_alg_anls_info", body=json.dumps(results))
        response = self.http_client.getresponse()
        self.logger.info("{} {} {}".format(response.status, response.reason, response.read()))

        f = self.mrms_sftp_manager.get_client().open(
            "{}/MARS_{}_{}.info".format(Constants.DIR_DIVISION_PATH, self.job_id, idx),
            "w"
        )
        f.write(json.dumps(results, indent=2))
        f.close()





if __name__ == '__main__':
    dam = MARSManager("ID", "0")
