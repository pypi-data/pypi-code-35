import threading
from logging import Logger

from sidecar.apps_configuration_end_tracker import AppsConfigurationEndTracker
from sidecar.aws_session import AwsSession
from sidecar.const import DateTimeProvider
from sidecar.health_check.app_health_check_state import AppHealthCheckState
from sidecar.sandbox_start_time_updater import ISandboxStartTimeUpdater
from sidecar.aws_status_maintainer import AWSStatusMaintainer


class AwsSandboxStartTimeUpdater(ISandboxStartTimeUpdater):
    def __init__(self, app_health_check_state: AppHealthCheckState,
                 sandbox_id: str, aws_session: AwsSession,
                 date_time_provider: DateTimeProvider,
                 logger: Logger,
                 apps_configuration_end_tracker: AppsConfigurationEndTracker,
                 aws_status_maintainer: AWSStatusMaintainer):
        super(AwsSandboxStartTimeUpdater, self).__init__(app_health_check_state, date_time_provider, logger, apps_configuration_end_tracker)
        self.aws_session = aws_session
        self.sandbox_id = sandbox_id
        self._date_time_provider = date_time_provider
        self._logger = logger
        self._cfclient = self.aws_session.get_cf_client()
        self.aws_status_maintainer = aws_status_maintainer

    def _on_health_check_done(self):
        threading.Thread(target=self._wait_for_stack_complete, args=()).start()

    def _wait_for_stack_complete(self):
        stack_name = self.aws_session.stack_name
        waiter = self._cfclient.get_waiter('stack_create_complete')
        self._logger.info(f'waiting for stack "{stack_name}" to reach stack_create_complete state')
        waiter.wait(StackName=stack_name)
        self._logger.info('stack completed!')
        self._update_sidecar_start_time()

    def _update_sidecar_start_time(self):
        self.aws_status_maintainer.update_sandbox_start_status(self._date_time_provider.get_current_time_utc())
