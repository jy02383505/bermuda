#! -*- coding=utf-8 -*-
import logging
from util.update_cms_device_status import main_fun

LOG_FILENAME = '/Application/bermuda/logs/update_cms_device_status.log'
logging.basicConfig(filename=LOG_FILENAME,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger('update_cms_device_status')
logger.setLevel(logging.DEBUG)


def main():
    logger.debug("update_cms_device_status begining...")
    main_fun()
    logger.debug("update_cms_device_status end...")


if __name__ == "__main__":
    main()
