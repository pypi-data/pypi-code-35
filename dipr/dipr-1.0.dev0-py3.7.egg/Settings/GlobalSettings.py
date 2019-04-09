
from pathlib import Path

from Settings.RepoSettings import RepoSettings


class GlobalSettings(object):

    TEMPLATE_DIRECTORY = "Templates"

    def __init__(self, dip_path):
        self.dip_path = Path(dip_path)
        self.dip_template_directory = Path(self.dip_path, GlobalSettings.TEMPLATE_DIRECTORY)
        self.dip_src_template_file_path = Path(self.dip_template_directory, RepoSettings.DIPR_SRC_FILE)
        self.dip_dep_template_file_path = Path(self.dip_template_directory, RepoSettings.DIPR_DEP_FILE)
        self.dip_sub_template_file_path = Path(self.dip_template_directory, RepoSettings.DIPR_SUB_FILE)

