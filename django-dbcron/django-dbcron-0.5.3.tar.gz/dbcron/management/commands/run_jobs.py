from io import StringIO
from dbcron.management.commands import _base
from dbcron import models


class Command(_base.Command):
    def add_arguments(self, parser):
        parser.add_argument(
            'job_ids', nargs='+',
            help="Job's IDs"
        )
        parser.add_argument(
            '-q', '--quiet', action='store_true',
            help='Disable any output (except logs)',
        )

    def handle(self, *args, **options):
        if options['quiet']:
            self.stdout = self.stdout = StringIO()
        jobs = models.Job.objects.filter(id__in=options['job_ids'])
        self.stdout.write(self.style.SUCCESS('Started run'))
        for job in jobs:
            self.stdout.write(self.style.SUCCESS('Started %s' % job.name))
            try:
                job.run()
                self.stdout.write(self.style.SUCCESS('Done %s' % job.name))
            except Exception as err:
                self.logger.exception("error with %s", job.name)
                continue
        self.stdout.write(self.style.SUCCESS('Done'))
