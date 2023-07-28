# GitHub Action to check if change log entry conforms to given rules in plain text file

[![CI Status](https://github.com/scientific-python/action-check-changelogfile/workflows/CI/badge.svg)](https://github.com/scientific-python/action-check-changelogfile/actions) [![Coverage](https://codecov.io/gh/scientific-python/action-check-changelogfile/branch/main/graph/badge.svg)](https://codecov.io/gh/scientific-python/action-check-changelogfile)

Check if a change log entry is present. If present, whether it is in the
expected section given the milestone. If not, whether it is allowed to
be missing or not. Create a `.github/workflows/check_changelog_entry.yml`
with this:

```
name: Check PR change log

on:
  pull_request:
    types: [opened, synchronize, labeled, unlabeled]

jobs:
  changelog_checker:
    name: Check if change log entry is correct
    runs-on: ubuntu-latest
    steps:
    - name: Check change log entry
      uses: scientific-python/action-check-changelogfile@0.2
      env:
        CHANGELOG_FILENAME: CHANGES.rst
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Note that adding the environment variable `CHECK_MILESTONE: false` (or anything other than `true`)
will cause the milestone check to be skipped.

Labels can be applied to the pull request to control its outcome:

* `skip-changelog-checks`: This results in success regardless; same as
  skipping the check altogether.
* `no-changelog-entry-needed`: This results in failure if a change log entry
  is present and success if it is missing. Use this label when the change log
  is decidedly not needed no matter what.
* `Affects-dev`: This results in failure if a change log entry is present and
  success if it is missing. This is because a change to an unreleased change
  does not require a change log.

Other ways this action can fail:

* Change log file is missing. This file is assumed to be `CHANGES.rst` but
  can be overwritten by `CHANGELOG_FILENAME` environment variable.
* Change log entry is present in multiple version sections.
* Change log entry is present but no milestone is set.
* Change log entry is under a version section that is inconsistent with the
  milestone set.
* Change log entry is missing and no special label (see above) is applied to
  indicate that it is expected to be missing.

#### How to run parser locally

While this is not an installable package, you are still able to run the parser
function if you have this repository checked out locally and you are in the
same directory as the parser module. Example usage:

```
>>> from core import load
>>> changes = load('path/to/CHANGES.rst')
>>> changes.versions
['0.1',
 '0.2',
 '0.2.1',
 '0.2.2',
 '0.2.3',
 ...]
>>> changes.issues
[256,
 272,
 291,
 293,
 296,
 ...]
>>> changes.versions_for_issue(4242)
['1.2']
>>> changes.issues_for_version('2.0.7')
[7411, 7248, 7402, 7422, 7469, 7486, 7453, 7493, 7510, 7493]
```

#### Format specification

The current format uses reStructuredText. Changelog entries should be given as
bullet point items inside sections for each version. These sections should have
a title with the following syntax:

```
    version (release date)
```

The release date can be `unreleased` if the version is not released yet.

The version sections can optionally include sub-sections in which the bullet
items are organized, and the file can also optionally include an overall title.

#### Why is this not written in TypeScript?

Writing this in TypeScript would make it run much faster. Unfortunately,
this Action depends on custom change log check logic, which was implemented in
Python. Therefore, this Action is best done in Python as well and needs
Docker to run.

In its current state, it probably takes about 20-30 seconds.
Fortunately, this Action can be run in parallel to the regular CI
workflow. A typical CI takes much longer than 30 seconds anyway,
so the overhead of running this Action should not be a blocker.
