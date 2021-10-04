# coding: utf-8

from traitlets import Type, Instance, default
from nbgrader.apps import ExportApp as BaseExportApp
from nbgrader.coursedir import CourseDirectory
from ..plugins import CustomExportPlugin, CanvasCsvExportPlugin
from nbgrader.api import Gradebook

aliases = {
    'log-level' : 'Application.log_level',
    'db': 'CourseDirectory.db_url',
    'to' : 'CanvasCsvExportPlugin.to',
    'canvas_export' : 'CanvasCsvExportPlugin.canvas_export',
    'exporter': 'ExportApp.plugin_class',
    'assignment' : 'CanvasCsvExportPlugin.assignment',
    'student': 'CanvasCsvExportPlugin.student',
    'course': 'CourseDirectory.course_id'
}
flags = {}


class ExportApp(BaseExportApp):

    name = u'async_nbgrader-export'

    aliases = aliases

    plugin_class = Type(
        CanvasCsvExportPlugin,
        klass=CustomExportPlugin,
        help="The plugin class for exporting the grades."
    ).tag(config=True)

    @default("classes")
    def _classes_default(self):
        classes = super(ExportApp, self)._classes_default()
        classes.append(ExportApp)
        classes.append(CustomExportPlugin)
        return classes

    def start(self):
        super(ExportApp, self).start()
        self.init_plugin()
        with Gradebook(self.coursedir.db_url, self.coursedir.course_id) as gb:
            self.plugin_inst.export(gb)
