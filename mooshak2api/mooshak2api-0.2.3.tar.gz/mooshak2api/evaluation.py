import requests

from mooshak2api.factory import GenericObject


class Evaluation(GenericObject):
    type = "evaluation_summary"
    status = "not_fetched"

    def __init__(self, contest_id, problem_id):
        super(Evaluation, self).__init__()
        self.contest_id = contest_id
        self.problem_id = problem_id

    def refresh(self, connection):
        """
        Refreshes the data from the server
        :param connection:
        :return:
        """
        r = requests.get(
            f"{connection.endpoint}data/contests/{self.contest_id}/submissions/{self.id}/evaluation-summary",
            headers=connection.headers_with_auth()
        )
        self.load_from_dict(r.json())

    @property
    def notify_type(self) -> str:
        """
        Returns the 'notification type' of the message, being one of:
             - success (Green)
             - warning (Amber/Orange)
             - error (Red)
             - info (blue)
        This is based from self.status. If they is no status, then 'none' will be returned
        :return: str: notify_type
        """
        status = dict(
            error_status={"Compile Time Error", "Invalid Exit Value", "Invalid Function", "Invalid Submission",
                          "Memory Limit Exceeded", "Output Limit Exceeded", "Presentation Error",
                          "Program Size Exceeded", "Requires Reevaluation", "Runtime Error", "Time Limit Exceeded"},
            warning_status={"Wrong Answer", "Evaluation Skipped"},
            success_status={"Accepted"},
            info_status={"Evaluating"}
        )
        if not hasattr(self, "status") or self.status is None:
            return None
        if self.status in status["success_status"]:
            return 'success'
        if self.status in status["error_status"]:
            return 'error'
        if self.status in status["warning_status"]:
            return 'warning'
        if self.status in ["info_status"]:
            return 'info'
        raise Exception(f"{self.status} is not a valid status for an Evaluation")
