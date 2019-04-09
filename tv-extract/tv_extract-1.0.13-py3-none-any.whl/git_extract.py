import csv
import logging
import os
import pickle

from collections import defaultdict
from pathlib import Path
from shutil import copyfile, rmtree

from .util.cd import cd
from .data import Config, Extract, PullRequest, Repo, Revision, RevisionGraph
from .gitextractor import extract_revision_graph, extract_pr_data
from .gitextractor.loc_cache import PickleCache


class _FileHandles:  # pragma: no cover
    def __init__(self, output_dir):
        self.author_totals_info = open(os.path.join(output_dir, 'author_totals.csv'), 'w', encoding='utf8')
        self.author_totals_info_writer = csv.writer(self.author_totals_info)
        self.author_totals_info_writer.writerow(["Repo", "Author", "Commits"])

        self.revision_info = open(os.path.join(output_dir, 'revs.csv'), 'w', encoding='utf8')
        self.revision_info_writer = csv.writer(self.revision_info)
        self.revision_info_writer.writerow(['Repo', 'CommitHash', 'TimeStamp', 'TimeZone', 'Author', 'AuthorEmail',
                                            'Domain', 'MergeToMaster'])

        self.loc_info = open(os.path.join(output_dir, 'loc.csv'), 'w', encoding='utf8')
        self.loc_info_writer = csv.writer(self.loc_info)
        self.loc_info_writer.writerow(['Repo', 'CommitHash', 'TimeStamp', 'Language', 'Files', 'Lines', 'Code',
                                       'Comments', 'Blanks'])

        self.loc_delta = open(os.path.join(output_dir, 'loc_delta.csv'), 'w', encoding='utf8')
        self.loc_delta_writer = csv.writer(self.loc_delta)
        self.loc_delta_writer.writerow(['Repo', 'CommitHash', 'TimeStamp', 'Author', 'Language', 'Files', 'Lines',
                                        'Code', 'Comments', 'Blanks', 'Revision Comment'])

        self.repo_info = open(os.path.join(output_dir, 'repo.csv'), 'w', encoding='utf8')
        self.repo_info_writer = csv.writer(self.repo_info)
        self.repo_info_writer.writerow(['Repo', 'Language', 'Files', 'Lines',
                                        'Code', 'Comments', 'Blanks'])

        self.prs_info = open(os.path.join(output_dir, 'prs.csv'), 'w', encoding='utf8')
        self.prs_info_writer = csv.writer(self.prs_info)
        self.prs_info_writer.writerow(['Repo', 'CommitHash', 'TimeStamp', 'ParentHashMaster', 'ParentHashBranch',
                                       'PrMergeDuration'])

    def close(self):
        self.author_totals_info.close()
        self.revision_info.close()
        self.loc_info.close()
        self.loc_delta.close()
        self.repo_info.close()
        self.prs_info.close()

class GitExtractor():
    def __init__(self, extract: Extract, output_dir: str, cache_dir):
        self.extract: Extract = extract
        self.files: _FileHandles = None
        self.output_dir = output_dir
        self.begin, self.end = extract.get_begin_end_timestamps()
        self.cache_dir = cache_dir
        self.projectname = ''

    def __enter__(self): # pragma: no cover
        self.files = _FileHandles(self.output_dir)

    def __exit__(self, exc_type, exc_val, exc_tb): # pragma: no cover
        self.files.close()

    def collect(self, repo_cache: Path, repo: Repo): # pragma: no cover
        self.projectname = repo.name
        with cd(str(repo_cache / repo.name)):
            cache = PickleCache(self.cache_dir / f'{repo.name}.cache_data.pkl')
            graph = extract_revision_graph(cache)
            self.process_graph(graph)
            cache.save_to_cache(graph)

    def process_graph(self, graph):
        self.extract_total_authors(graph)
        self.extract_pr_info(graph)
        self.extract_code_info(graph)
        self.extract_revision_info(graph)

    def load_from_cache(self, graph: RevisionGraph, cache: Path): # pragma: no cover
        if cache and cache.exists():
            cache_data = pickle.load(cache.open(mode='rb'))
            for key, data in cache_data.items():
                graph.revisions[key].file_infos = data[0]

    def save_to_cache(self, graph: RevisionGraph, cache: Path): # pragma: no cover
        if cache and cache.exists():
            cache_data = {} # key by revision id, values tuple of: file_infos and deltas
            for key, revision in graph.revisions.items():
                if revision.file_infos or revision.delta:
                    cache_data[key] = [revision.file_infos, revision.delta]
            pickle.dump(cache_data, cache.open(mode='wb'))

    def extract_total_authors(self, graph):

        authors = defaultdict(int)
        # exclude merges from calculating author totals
        for rev_hash in graph.not_a_merge:
            rev = graph.revisions[rev_hash]
            if rev.stamp >= self.begin and rev.stamp <= self.end:
                authors[rev.author] += 1

        for author, total_commits in authors.items():
            self.files.author_totals_info_writer.writerow([self.projectname, author, total_commits])

    def extract_pr_info(self, graph):
        def row_processor(row: PullRequest):
            if row.stamp >= self.begin and row.stamp <= self.end:
                self.files.prs_info_writer.writerow([self.projectname, row.hash, row.stamp, row.master_rev,
                                                        row.branch_rev, row.duration.total_seconds()])
        extract_pr_data(row_processor, graph)

    def extract_code_info(self, graph):
        rev_max: Revision = None
        for rev_hash in graph.not_a_merge:
            revision: Revision = graph.revisions[rev_hash]
            if not rev_max or revision.stamp > rev_max.stamp:
                rev_max = revision
            if revision.stamp >= self.begin and revision.stamp <= self.end:
                for lang, file_info in revision.delta.items():
                        if file_info.file_count or \
                                file_info.line_count or \
                                file_info.code_line_count or \
                                file_info.comment_line_count or \
                                file_info.blank_line_count:

                                self.files.loc_delta_writer.writerow([
                                    self.projectname,
                                    revision.hash,
                                    revision.stamp,
                                    revision.author,
                                    lang,
                                    file_info.file_count,
                                    file_info.line_count,
                                    file_info.code_line_count,
                                    file_info.comment_line_count,
                                    file_info.blank_line_count,
                                    revision.comments
                                ])
        for rev_hash in graph.master_revs:
            revision: Revision = graph.revisions[rev_hash]
            if not rev_max or revision.stamp > rev_max.stamp:
                rev_max = revision
            if revision.stamp >= self.begin and revision.stamp <= self.end:
                for lang, file_info in revision.file_infos.items():
                        if file_info.file_count or \
                                file_info.line_count or \
                                file_info.code_line_count or \
                                file_info.comment_line_count or \
                                file_info.blank_line_count:

                            self.files.loc_info_writer.writerow([
                                self.projectname,
                                revision.hash,
                                revision.stamp,
                                lang,
                                file_info.file_count,
                                file_info.line_count,
                                file_info.code_line_count,
                                file_info.comment_line_count,
                                file_info.blank_line_count
                            ])

        if rev_max:
            for file_info in rev_max.file_infos.values():
                self.files.repo_info_writer.writerow([self.projectname,
                                                      file_info.language,
                                                      file_info.file_count,
                                                      file_info.line_count,
                                                      file_info.code_line_count,
                                                      file_info.comment_line_count,
                                                      file_info.blank_line_count])

    def extract_revision_info(self, graph):
        for revision in graph.revisions.values():
            if revision.stamp >= self.begin and revision.stamp <= self.end:
                self.files.revision_info_writer.writerow([self.projectname,
                                                          revision.hash,
                                                          revision.stamp,
                                                          revision.timezone,
                                                          revision.author,
                                                          revision.email,
                                                          revision.domain,
                                                          1 if revision.is_a_pr else 0])


def update_repo(git, repo: Repo, repo_cache: Path):
    repo_dir = repo_cache / repo.name
    if repo_dir.exists():
        try:
            git_repo = git.Repo(str(repo_dir))
            origin = git_repo.remotes.origin
            origin.fetch()
            origin.pull()
        except git.exc.GitCommandError:
            rmtree(str(repo_dir))
            git.Repo.clone_from(repo.remote, str(repo_dir))
    else:
        git.Repo.clone_from(repo.remote, repo_dir)

def handle_repo_mailmap(repo, repo_cache, mailmap_file) -> Path:
    # do this here to avoid errors during import if git isn't installed and other aspects of tv-extract are used
    import git
    logging.info(f"Updating repo: {repo.name}")
    update_repo(git, repo, repo_cache)
    repo_mailmap_file = repo_cache / repo.name / '.mailmap'
    if mailmap_file and mailmap_file.exists():
        if repo_mailmap_file.exists():
            logging.info(f"Appending mailmap from config to repo: {repo_mailmap_file}")
            with repo_mailmap_file.open(mode='a+') as file:
                with mailmap_file.open(mode='r') as input:
                    file.write("\n")
                    file.write(input.read())
            repo_mailmap_file = None
        else:
            logging.info(f"Copying mailmap from config to repo: {repo_mailmap_file}")
            copyfile(mailmap_file, repo_mailmap_file)
    else:
        logging.info("No mailmap to handle")
        repo_mailmap_file = None
    return repo_mailmap_file


def git_extract(config: Config, cache_root: Path) -> None:

    # first run through all extracts defined in config and update all gitextractor repos for those extracts
    # including adding the specified mailmap file to the repo, or extending an existing mailmap file
    repo_cache = cache_root / 'repos'
    repo_cache.mkdir(parents=True, exist_ok=True)
    mailmap_file = None
    if config.mailmap_file:
        mailmap_file = Path(config.mailmap_file)

    extract_cache_dir = cache_root / 'extracts'
    extract_cache_dir.mkdir(parents=True, exist_ok=True)

    for extract in config.extracts:
        extract_path = Path(config.output_path) / extract.name
        extract_path.mkdir(parents=True, exist_ok=True)
        extractor = GitExtractor(extract, str(extract_path), extract_cache_dir)
        with extractor:
            for repo in extract.repos:
                logging.info(f'********************* Creating Git Extract: {repo.name} *********************')
                try:
                    repo_mailmap_file = handle_repo_mailmap(repo, repo_cache, mailmap_file)
                    extractor.collect(repo_cache, repo)
                    if repo_mailmap_file:
                        logging.info(f'Deleting temporary mailmap file: {repo_mailmap_file}')
                        repo_mailmap_file.unlink()
                except:
                    logging.exception(f"Unexpected error processing {repo.name}. Continuing...")

