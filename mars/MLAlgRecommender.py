import time
from mars.common.Singleton import Singleton
from mars.common.thread.KubePodSafetyTermThread import KubePodSafetyTermThread
from mars.common.Common import Common
from mars.manager.MARSManager import MARSManager


class MLAlgRecommender(KubePodSafetyTermThread, metaclass=Singleton):
    def __init__(self, job_id: str, job_idx: str):
        KubePodSafetyTermThread.__init__(self)
        self.logger = Common.LOGGER.get_logger()

        self.mars_manager = MARSManager(job_id, job_idx)

        self.logger.info("MLAlgRecommender Initialized!")

    def run(self) -> None:
        while not self.mars_manager.get_terminate():
            self.mars_manager.recommend()
            time.sleep(1)

        self.logger.info("MLAlgRecommender terminate!")


if __name__ == '__main__':
    import sys

    j_id = sys.argv[1]
    j_idx = sys.argv[2]

    mars = MLAlgRecommender(j_id, j_idx)
    mars.start()
    mars.join()
