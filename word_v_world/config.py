from pathlib import Path
import socket

from ludwig.config import mnt_point


class RemoteDirs:
    """
    Typically, when using LudwigCluster to execute code, root should always be /media/research_data
     regardless of user's OS.
    However, when user intends to execute code on host only, and intends to retrieve data from shared drive,
     and has MacOS, root must be changed to something like /Volumes/research_data

    """
    research_data = Path(mnt_point) / 'research_data'
    root = research_data / 'Word_V_World'
    runs = root / 'runs'
    wiki = research_data / 'CreateWikiCorpus'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'word_v_world'
    runs = root / '{}_runs'.format(src.name)

    # TODO this is a hack - use .env file and dot_env package to remedy

    if socket.gethostname() == 'wirelessprv-10-195-203-206.near.illinois.edu':
        wiki = Path('/Volumes/GoogleDrive/My Drive/UIUC/PyCharm') / 'CreateWikiCorpus'
    elif socket.gethostname() == 'Emilys-MacBook-Pro.local':
        wiki = Path('/Volumes/GoogleDrive/My Drive/UIUC/PyCharm') / 'CreateWikiCorpus'
    else:
        wiki = Path('/home/ph/CreateWikiCorpus')


class Global:
    debug = False


class Default:

    # if this does not work, check the defaults that are added from createwikicorpus.params
    param2requests = {'part': [0, 1, 2, 3, 4, 5],
                      'num_machines': [6],
                      'no_templates': [True],
                      'filter_disambig_pages': [True],
                      'input_file_name': ['enwiki-20190920-pages-articles-multistream.xml.bz2']}
