
from Protocols.Git.GitRepoHandler import GitRepoHandler
from Protocols.Hg.HgRepoHandler import HgRepoHandler

SUPPORTED_PROTOCOLS = [GitRepoHandler.GIT_ID, HgRepoHandler.HG_ID]

def resolve_repo_handler(resolved_repo=None, full_repo_path=None):
    """
    Given a resolved repo, find the protocol implementation it should use.  The caller may specify either a resolved
    repo object or a path to a repo on disk.  If a path is specified, the available functional command are limited to
    add, commit, tag, and push.
    :param resolved_repo: A previously resolved repo.
    :param full_repo_path: The path to a possible repo on disk but without the resolved info like revision, url, etc
    :return: A protocol provider or None if it can't find a match.
    """

    if resolved_repo:
        if resolved_repo.protocol == GitRepoHandler.GIT_ID:
            return GitRepoHandler(resolved_repo=resolved_repo, full_repo_path=full_repo_path)
        elif resolved_repo.protocol == HgRepoHandler.HG_ID:
            return HgRepoHandler(resolved_repo=resolved_repo, full_repo_path=full_repo_path)
        else:
            return None

    if full_repo_path:
        if GitRepoHandler.is_git_dir(full_repo_path):
            return GitRepoHandler(full_repo_path=full_repo_path)
        elif HgRepoHandler.is_hg_dir(full_repo_path):
            return HgRepoHandler(full_repo_path=full_repo_path)
        else:
            return None

    return None


