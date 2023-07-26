from rst_parser import RstChangelog

__all__ = ['load', 'loads']


def load(filename, format='rst'):
    """
    Parse a changelog file.

    Parameters
    ----------
    filename : str
        The changelog file
    format : { 'rst' }
        The format of the changelog file (only rst is supported at this time)
    """
    if format == 'rst':
        changelog = RstChangelog()
        changelog.parse_file(filename)
        return changelog
    else:
        raise ValueError(f'Format not recognized: {format}')


def loads(text, format='rst'):
    """
    Parse a changelog string.

    Parameters
    ----------
    text : str
        The changelog string
    format : { 'rst' }
        The format of the changelog file (only rst is supported at this time)
    """
    if format == 'rst':
        changelog = RstChangelog()
        changelog.parse_string(text)
        return changelog
    else:
        raise ValueError(f'Format not recognized: {format}')
