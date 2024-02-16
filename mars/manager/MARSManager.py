# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.

import json
from typing import Union

import requests as rq
from pycmmn.sftp.SFTPClientManager import SFTPClientManager

from mars.common.Common import Common
from mars.common.Constants import Constants
from mars.recommender.RandomRecommender import RandomRecommender


class MARSManager(object):
    # class : DataAnalyzerManager
    def __init__(self, job_id, job_idx):
        self.logger = Common.LOGGER.getLogger()

        self.mrms_sftp_manager: Union[SFTPClientManager, None] = None

        self.rest_root_url = f"http://{Constants.MRMS_SVC}:{Constants.MRMS_REST_PORT}"

        self.job_id = job_id
        self.current = 0
        self.logger.info("MARSManager initialized.")

    def initialize(self):
        self.mrms_sftp_manager = SFTPClientManager(
            "{}:{}".format(Constants.MRMS_SVC, Constants.MRMS_SFTP_PORT),
            Constants.MRMS_USER,
            Constants.MRMS_PASSWD,
            self.logger,
        )

    def load_job_info(self, filename):
        return self.mrms_sftp_manager.load_json_data(filename)

    def recommend(self):
        filename = f"{Constants.DIR_JOB_PATH}/{self.job_id}/DPRS_{self.job_id}_{self.current}.info"
        project_tag_list = rq.get(f"{self.rest_root_url}/mrms/get_project_tag?project_id={self.job_id}").text.split(",")
        if self.mrms_sftp_manager.is_exist(filename):
            job_info = self.load_job_info(filename)
            results = list()
            for dprs_data in job_info:
                data_analysis_id: str = dprs_data.get("data_analysis_id")
                dataset_format = self.get_dataset_format(data_analysis_id)
                results += RandomRecommender(
                    project_purpose_cd=dprs_data.get("project_purpose_cd", None), project_tag_list=project_tag_list
                ).recommend(dprs_data, self.job_id, dataset_format)
                self.logger.debug(f"project_id: {self.job_id}, recommended: {results[-1]}")

            response = rq.post(f"{self.rest_root_url}/mrms/insert_alg_anls_info", json=results)
            self.logger.info(f"insert alg anls info: {response.status_code} {response.reason} {response.text}")

            tmp_filename = f"{Constants.DIR_JOB_PATH}/{self.job_id}/MARS_{self.job_id}_{self.current}"
            f = self.mrms_sftp_manager.get_client().open(f"{tmp_filename}.tmp", "w")
            f.write(json.dumps(results, indent=2))
            f.close()
            self.mrms_sftp_manager.rename(f"{tmp_filename}.tmp", f"{tmp_filename}.info")
            self.current += 1

    def get_dataset_format(self, data_analysis_id) -> str:
        response = rq.get(f"{self.rest_root_url}/mrms/get_dataset_format?data_analysis_id={data_analysis_id}")
        format_type = response.text.replace("\n", "")
        self.logger.info(f"get data anlaysis id: {response.status_code} {response.reason} {response.text}")
        return format_type

    def update_project_status(self, status):
        status_json = {"status": status, "project_id": self.job_id}
        response = rq.post(f"{self.rest_root_url}/mrms/update_projects_status", json=status_json)
        self.logger.info(f"update project status: {response.status_code} {response.reason} {response.text}")

    def get_terminate(self) -> bool:
        response = rq.get(f"{self.rest_root_url}/mrms/get_proj_sttus_cd?project_id={self.job_id}")
        status = response.text.replace("\n", "")
        if status == Constants.STATUS_PROJECT_COMPLETE or status == Constants.STATUS_PROJECT_ERROR:
            return True
        return False

    def terminate(self):
        if self.mrms_sftp_manager is not None:
            self.mrms_sftp_manager.close()


if __name__ == "__main__":
    dam = MARSManager("ID", "0")
