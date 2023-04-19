# This Action is minimally maintained

`astropy` has switched to using `towncrier`, so this Action is no longer relevant for that repo
but some smaller projects are still using this.

# GitHub Action to check if change log entry conforms to pre-towncrier Astropy format

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
      uses: pllim/action-check_astropy_changelog@main
      env:
        CHANGELOG_FILENAME: CHANGES.rst
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Note that adding the environment variable `CHECK_MILESTONE: false` (or anything other than `true`)
will cause the milestone check to be skipped.

This action uses [astropy-changelog](https://github.com/astropy/astropy-changelog) to parse the change log.

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

#### Why is this not written in TypeScript?

Writing this in TypeScript would make it run much faster. Unfortunately,
this Action depends on `astropy-changelog`, which was implemented in
Python. Therefore, this Action is best done in Python as well and needs
Docker to run.

Furthermore, Astropy might change its change log format in the
future. With that in mind, there is not much motivation to
rewrite the logic in `astropy-changelog` in TypeScript.

In its current state, it probably takes about 20-30 seconds.
Fortunately, this Action can be run in parallel to the regular CI
workflow. A typical CI takes much longer than 30 seconds anyway,
so the overhead of running this Action should not be a blocker.
