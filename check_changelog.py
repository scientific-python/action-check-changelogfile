import json
import os
import sys

from astropy_changelog import loads
from github import Github

event_jsonfile = os.environ['GITHUB_EVENT_PATH']

with open(event_jsonfile, encoding='utf-8') as fin:
    event = json.load(fin)

event = event['event']
pr_labels = [e['name'] for e in event['pull_request']['labels']]

if 'skip-changelog-checks' in pr_labels:
    print('Changelog checks manually disabled for this pull request.')
    sys.exit(0)  # Green but no-op

forkrepo = event['pull_request']['head']['repo']['full_name']
pr_branch = event['pull_request']['head']['ref']
g = Github(os.environ.get('GITHUB_TOKEN'))

clog_file = os.environ.get('CHANGELOG_FILENAME', 'CHANGES.rst')
repo = g.get_repo(forkrepo)
try:
    contents = repo.get_contents(clog_file, ref=pr_branch)
except Exception:
    print('This repository does not appear to have a change log! '
          f'(Expecting a file named {clog_file})')
    sys.exit(1)

# Parse changelog
changelog = loads(contents.decoded_content.decode('utf-8'))

# Find versions for the pull request we are looking at
pr_num = event['number']
versions = changelog.versions_for_issue(pr_num)

if len(versions) > 1:
    print('Change log entry present in multiple version sections '
          f'({", ".join(versions)}).')
    sys.exit(1)

if len(versions) == 1:
    version = versions[0]

    if 'no-changelog-entry-needed' in pr_labels:
        print(f'Changelog entry present in {version} but '
              '**no-changelog-entry-needed** label set.')
        sys.exit(1)

    if 'Affects-dev' in pr_labels:
        print(f'Changelog entry present in {version} but '
              '**Affects-dev** label set.')
        sys.exit(1)

    base_repo = event['pull_request']['base']['repo']['full_name']
    repo = g.get_repo(base_repo)
    pr = repo.get_pull(pr_num)

    if not pr.milestone:
        print(f'Cannot check for consistency of change log in {version} since '
              'milestone is not set.')
        sys.exit(1)

    milestone = pr.milestone.title
    if milestone.startswith('v'):
        milestone = milestone[1:]

    if version.startswith('v'):
        version = version[1:]

    if milestone != version:
        print(f'Changelog entry section ({version}) '
              f'inconsistent with milestone ({milestone}).')
        sys.exit(1)

    print(f'Changelog entry consistent with milestone ({milestone}).')

else:  # No change log found
    if 'Affects-dev' in pr_labels:
        print('Changelog entry not present, as expected since the '
              '**Affects-dev** label is present.')
    elif 'no-changelog-entry-needed' in pr_labels:
        print('Changelog entry not present, as expected since the '
              '**no-changelog-entry-needed** label is present')
    else:
        print('Changelog entry not present, (or PR number missing) and '
              'neither the **Affects-dev** nor the '
              '**no-changelog-entry-needed** label is set.')
        sys.exit(1)
