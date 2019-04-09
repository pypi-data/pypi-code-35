import time
from io import StringIO
from concurrent import futures

from dbcron.management.commands import _base
from dbcron import models
from dbcron import settings


class Command(_base.Command):
    def add_arguments(self, parser):
        parser.add_argument(
            '-t', '--tags', nargs='*',
            help='Filter jobs by tag(s)'
        )
        parser.add_argument(
            '-q', '--quiet', action='store_true',
            help='Disable any output (except logs)',
        )

    def stop(self):
        """Helper for tests"""
        return False

    def run_job(self, job):
        """Decides to run a job, launches it and handles errors."""
        # Time decision
        next_ = int(job.entry.next())
        if next_ != 0:
            self.logger.debug("%s will run in %ssec", job.name, next_)
            return
        # Run
        self.logger.info("started %s", job.name)
        try:
            result = job.run()
        except Exception as err:
            self.logger.exception("error with %s", job.name)
            raise
        finally:
            self.logger.info("finished %s", job.name)
        return result

    def main(self, executor, tags, **kwargs):
        """Infinite loop acting as cron daemon."""
        # Lazy filtering
        jobs = models.Job.objects.filter(is_active=True)
        if tags:
            jobs = jobs.filter(tag__in=tags)
        self.stdout.write(self.style.SUCCESS('Started'))
        # Main Loop
        while True:
            self.logger.debug("new loop")
            executor.map(self.run_job, jobs.all())
            if self.stop():
                break
            time.sleep(1)

    def handle(self, *args, **options):
        if options['quiet']:
            self.stdout = self.stdout = StringIO()
        executor = futures.ThreadPoolExecutor(max_workers=settings.MAX_WORKERS)
        try:
            self.main(executor, **options)
        except KeyboardInterrupt as err:
            executor.shutdown()
            self.stdout.write(self.style.WARNING('Stopped'))
            return
