import os
import shutil
import contextlib
import tempfile

from pip._internal.req import parse_requirements
from pip._internal.download import is_file_url, is_dir_url, is_vcs_url
from pip._internal.index import PackageFinder
from pip._internal.operations.prepare import RequirementPreparer
from pip._internal.req.req_tracker import RequirementTracker
from pip._vendor.requests import Session

from .compat import get_dist_from_abstract_dist


@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield d
    finally:
        if os.path.exists(d):
            shutil.rmtree(d)


def link_req_to_str(req):
    url = req.link.url.encode("utf8")
    if req.editable:
        return b"-e " + url
    else:
        return url


class RequirementsParser:
    def __init__(self):
        self.session = Session()
        self.finder = PackageFinder(
            find_links=[],
            index_urls=[],
            session=self.session,
        )
        self.preparer = RequirementPreparer(
            build_dir=None,
            download_dir=None,
            src_dir=None,
            wheel_download_dir=None,
            progress_bar=None,
            build_isolation=True,
            req_tracker=RequirementTracker(),
        )

    def _get_local_deps(self, req):
        abstract_dist = self.preparer.prepare_editable_requirement(
            req, [], False, self.finder
        )

        dist = get_dist_from_abstract_dist(abstract_dist, self.finder)
        return dist.requires(req.extras)

    def _process_requirement(self, req):
        ext_reqs, loc_reqs = [], []
        if req.link:
            if is_vcs_url(req.link):
                # TODO: Is this needed or even supported?
                raise NotImplementedError(
                    "Requirement `{}` is not in a supported format".format(
                        str(req)
                    )
                )
            elif is_file_url(req.link):
                if is_dir_url(req.link):
                    loc_reqs.append(link_req_to_str(req))
                    for subreq in self._get_local_deps(req):
                        ext_reqs.append(str(subreq).encode("utf-8"))
                else:
                    # TODO: Is this needed or even supported?
                    raise NotImplementedError(
                        "Requirement `{}` is not in a supported format".format(
                            str(req)
                        )
                    )
            else:
                ext_reqs.append(link_req_to_str(req))
        else:
            ext_reqs.append(str(req.req).encode("utf8"))

        return ext_reqs, loc_reqs

    def parse(self, reqs_filepath):
        ext_reqs, loc_reqs = [], []
        for raw_req in parse_requirements(reqs_filepath, session=self.session):
            ext_subreqs, loc_subreqs = self._process_requirement(raw_req)
            ext_reqs.extend(ext_subreqs)
            loc_reqs.extend(loc_subreqs)
        return ext_reqs, loc_reqs
