import logging
import os

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.tornado import TornadoScheduler

jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")}

executors = {"default": ThreadPoolExecutor(int(os.environ.get('NBGRADER_THREADS', '1')))}

job_defaults = {
    "misfire_grace_time": None,  # to queue jobs which are triggered but no thread is available to run them,
    "coalesce": False,
}

scheduler = TornadoScheduler(
    jobstores=jobstores, executors=executors, job_defaults=job_defaults
)

scheduler_logger = logging.getLogger("apscheduler")

scheduler_logger.setLevel(logging.DEBUG)
