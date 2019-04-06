import json
import re
import os
from git import Repo
from collections import OrderedDict

CHANGELOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'changelog.json')

def generate_changelog():

    r = Repo('.')

    pattern = re.compile('(enh|fix): (.+)')

    data = OrderedDict()

    last_tag = None

    commit_hash_to_tag = {str(t.commit): (t.tag.tag, t.tag.tagged_date) for t in r.tags}

    for commit in r.iter_commits():

        commit_hex = commit.binsha.hex()

        if commit_hex in commit_hash_to_tag:
            (last_tag, last_tag_date) = commit_hash_to_tag[commit_hex]
            data[last_tag] = {'enh': [], 'fix': [], 'date': last_tag_date}

        if not last_tag:
            continue

        matches = pattern.match(commit.message.strip())
        if not matches:
            continue

        prefix, message = matches.groups()

        data[last_tag][prefix].append(message)

    with open(CHANGELOG_FILE_PATH, 'w') as f:
        json.dump([{'name': tag_name, **tag_data} for tag_name, tag_data in data.items()], f, indent=2)
