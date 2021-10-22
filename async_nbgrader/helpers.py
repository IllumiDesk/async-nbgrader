import contextlib
import os

from nbgrader.auth import Authenticator
from nbgrader.apps import NbGrader
from nbgrader.apps.api import NbGraderAPI
from nbgrader.coursedir import CourseDirectory
from nbgrader.exchange import ExchangeList
from jupyter_core.paths import jupyter_config_path


@contextlib.contextmanager
def chdir(dirname):
    currdir = os.getcwd()
    os.chdir(dirname)
    yield
    os.chdir(currdir)


@contextlib.contextmanager
def get_assignment_dir_config(notebook_dir):
    # first get the exchange assignment directory
    with chdir(notebook_dir):
        config = load_config()

    lister = ExchangeList(config=config)
    assignment_dir = lister.assignment_dir

    if assignment_dir == ".":
        assignment_dir = notebook_dir + "/.jupyter"

    # now cd to the full assignment directory and load the config again
    with chdir(assignment_dir):
        app = NbGrader()
        app.config_file_paths.append(os.getcwd())
        app.load_config_file()

        yield app.config


def load_config():
    paths = jupyter_config_path()
    paths.insert(0, os.getcwd())

    app = NbGrader()
    app.config_file_paths.append(paths)
    app.load_config_file()

    return app.config


def get_nbgrader_api(notebook_dir, course_id=None):
    with get_assignment_dir_config(notebook_dir) as config:
        if course_id:
            config.CourseDirectory.course_id = course_id

        coursedir = CourseDirectory(config=config)
        print("db_url='" + coursedir.db_url + "'")
        authenticator = Authenticator(config=config)
        api = NbGraderAPI(coursedir, authenticator)
        return api
