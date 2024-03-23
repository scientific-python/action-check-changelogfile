# Since this is not an installable package, these tests
# are meant to be run locally.

import os

from core import load, loads

DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')


def test_rst_parser():

    changelog = load(os.path.join(DATA_DIR, 'changes_core.rst'))

    assert changelog.versions == ['0.1', '3.0.1', '3.1', '3.2rc1']

    assert changelog.issues == [100, 102, 103, 104, 105, 106, 107, 108, 109, 110]

    assert changelog.issues_for_version('0.1') == []
    assert changelog.issues_for_version('3.0.1') == [104, 105, 106, 107, 108, 109]
    assert changelog.issues_for_version('3.1') == [100, 102, 103]
    assert changelog.issues_for_version('3.2rc1') == [110]

    for issue in [104, 105, 106, 107, 108, 109]:
        assert changelog.versions_for_issue(issue) == ['3.0.1']

    for issue in [100, 102, 103]:
        assert changelog.versions_for_issue(issue) == ['3.1']

    assert changelog.versions_for_issue(110) == ['3.2rc1']


def test_rst_parser_helpers_style():

    # The astropy-helpers changelog has an overall title and no sub-sections
    # within versions

    changelog = load(os.path.join(DATA_DIR, 'changes_with_title.rst'))

    assert changelog.versions == ['0.1', '1.0']

    assert changelog.issues == [100]

    assert changelog.issues_for_version('0.1') == []
    assert changelog.issues_for_version('1.0') == [100]
    assert changelog.versions_for_issue(100) == ['1.0']


SIMPLE_CHANGELOG = ('1.0 (2018-10-22)\n'
                    '----------------\n'
                    '* change1 [#1234]\n')


def test_short_rst():

    # Regression test for a bug that caused a changelog with only one version section to fail

    changelog = loads(SIMPLE_CHANGELOG)

    assert changelog.versions == ['1.0']
    assert changelog.issues == [1234]
