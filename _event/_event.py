import collections
import functools
import heapq
import json
import os.path
from typing import Union, List, Dict
from inspect import currentframe
from logging import Logger as Log
from _config import config, cli
from _common import _common
from _igithub import _github
from _util import _util_file
from _util import _util_common as _iutil_common_
import asyncio
from _connect import _connect as _connect_
from _util import _util_file as _file_
from pprint import pprint


def order_of_events(logger: Log = None) -> None:

    """Order of events, comprised of a list of steps needed to convert input json array into terraform input files


    Args:
        logger: Whether error msg should be persisted in a log file

    Returns:
        None

    """

    _object = _connect_.get_object("awss3")
    print(_object.list_buckets())

    # pprint(_object_ec2.describe_instance("i-0d1b3a6458dd564e0")
    # print(_object_s3.("ssh-082761530193-e2e-us-east-2",
    #                                encrypted_flg=True,
    #                                suffix_flg=None
    #                                ))










