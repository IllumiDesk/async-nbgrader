import traceback

from .helpers import get_nbgrader_api
from .scheduler import scheduler_logger


def autograde_assignment(
    notebook_dir: str,
    course_id:str = None,
    assignment_id:str = None,
    student_id: str = None,
):
    """Autograde an assignment asyncronously.

    Args:
        notebook_dir (str): the path and filename for the notebook directory.
        course_id (str, optional): The course id. Defaults to None.
        assignment_id (str, optional): The assignment id. Defaults to None.
        student_id (str, optional): The student id. Defaults to None.
    """
    job_info = f"notebook_dir={notebook_dir}, course_id = {course_id}, assignment_id={assignment_id}, student_id={student_id}"
    scheduler_logger.info(f"Initialize autograding app for {job_info}")
    try:
        api = get_nbgrader_api(notebook_dir, course_id)
        api.log = scheduler_logger
        scheduler_logger.info(f"Starting autograding for {job_info}")
        api.autograde(assignment_id, student_id)
        scheduler_logger.info(f"Completed autograding for {job_info}")
    except Exception as e:
        scheduler_logger.error(traceback.format_exc())
