import csv

from traitlets import Unicode
from nbgrader.api import MissingEntry
from nbgrader.plugins import BasePlugin

class CustomExportPlugin(BasePlugin):
    to = Unicode("", help="destination to export to").tag(config=True)
    canvas_import = Unicode("", help="src to read canvas data from").tag(config=True)

class CanvasCsvExportPlugin(CustomExportPlugin):
    """Canvas CSV exporter plugin."""

    def export(self, gradebook):
        if self.to == "":
            dest = "canvas_grades.csv"
        else:
            dest = self.to

        if self.canvas_import == "":
            canvas_import = "canvas.csv"
        else:
            canvas_import = self.canvas_import

        self.log.info("Exporting grades to %s", dest)

        with open(canvas_import, 'r') as csv_file, open(dest, 'w') as op_csv_file:
            csv_reader = csv.DictReader(csv_file)
            fields = csv_reader.fieldnames
            csv_writer = csv.DictWriter(op_csv_file, fields)
            csv_writer.writeheader()
            for row in csv_reader:
                if "Points Possible" in row['Student']:
                    self.log.info("Skipping second row")
                    csv_writer.writerow(row)
                    continue
                self.log.info("Finding student with ID %s", row['ID'])
                for column in fields:
                    if " (" not in column:
                        continue
                    assignment_name = column.split(" (")[0]
                    self.log.info("Finding submission of Student '%s' for Assignment '%s'", row['ID'], assignment_name)
                    submission = None
                    try:
                        submission = gradebook.find_submission(assignment_name, row['ID'])
                        row[column] = max(0.0, submission.score - submission.late_submission_penalty)
                    except MissingEntry:
                        self.log.info("Submission of Student '%s' for Assignment '%s' not found", row['ID'], assignment_name)
                        continue
                csv_writer.writerow(row)
