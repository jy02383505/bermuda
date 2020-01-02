# -*- coding:utf-8 -*-
"""
Created on 2018-11-29

"""
import os
from util.aps_server import run
from util import log_utils
import time


logger = log_utils.get_preload_Logger()


def main():
    logger.debug("aps_server begining...")
    run()
    logger.debug("aps_server end.")
    os._exit(0)  # fix :there are threads, not exit properly


if __name__ == "__main__":
    main()
