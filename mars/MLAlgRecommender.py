import time
from pycmmn.Singleton import Singleton
from pycmmn.KubePodSafetyTermThread import KubePodSafetyTermThread
from mars.common.Common import Common
from mars.common.Constants import Constants
from mars.manager.MARSManager import MARSManager


class MLAlgRecommender(KubePodSafetyTermThread, metaclass=Singleton):
    def __init__(self, job_id: str, job_idx: str):
        KubePodSafetyTermThread.__init__(self)
        self.logger = Common.LOGGER.getLogger()

        self.mars_manager = MARSManager(job_id, job_idx)
        try:
            self.mars_manager.initialize()
            self.logger.info("MLAlgRecommender Initialized!")
        except Exception as e:
            self.logger.error(e, exc_info=True)

    def run(self) -> None:

        while not self.mars_manager.get_terminate():
            try:
                self.mars_manager.recommend()
            except Exception as e:
                self.logger.error(e, exc_info=True)
                self.mars_manager.update_project_status(Constants.STATUS_PROJECT_ERROR)
            finally:
                time.sleep(10)

        self.logger.info("MLAlgRecommender terminate!")
        self.mars_manager.terminate()


if __name__ == '__main__':
    import sys

    j_id = sys.argv[1]
    j_idx = sys.argv[2]

    mars = MLAlgRecommender(j_id, j_idx)
    mars.start()
    mars.join()
