import random
from inspect import currentframe
from typing import List, Dict, Union
from logging import Logger as Log
from botocore.exceptions import ClientError
from _meta import _meta as _meta_
from _config import config as _config_
from _common import _common as _common_
from _aws import awsclient_config as _aws_config_
from _aws import awscommon
from _util import _util_common as _util_common_
from _util import _util_file as _util_file_
from pprint import pprint
from time import sleep


def ssm_rds_template(username: str,
                     password: str,
                     host: str,
                     dbClusterIdentifier: str,
                     engine: str = "aurora-mysql",
                     port: str = "3306",
                     logger: Log = None
                     ) -> Dict:
    try:
        _parameters = {"username": username,
                       "password": password,
                       "engine": engine,
                       "host": host,
                       "port": port,
                       "dbClusterIdentifier": dbClusterIdentifier}

        return _parameters
    except Exception as err:
        _common_.error_logger(currentframe().f_code.co_name,
                              f"require input values are {' '.join(list(_parameters.keys()))}",
                              logger=logger,
                              mode="error",
                              ignore_flag=False)


def ssm_default_template(secret_string: str, logger: Log = None) -> Dict:
    try:
        _parameters = {"secret_string": secret_string}
        return _parameters
    except Exception as err:
        _common_.error_logger(currentframe().f_code.co_name,
                              f"require input values are {' '.join(list(_parameters.keys()))}",
                              logger=logger,
                              mode="error",
                              ignore_flag=False)


class AwsApiSecretManager(metaclass=_meta_.Meta):
    def __init__(self, config: _config_.AwsApiConfigSingleton = None, logger: Log = None):
        self._config = config if config else _config_.AwsApiConfigSingleton()
        self._session = _aws_config_.setup_session_by_profile(self._config.config.get("aws_profile_name"),
                                                              self._config.config.get("aws_region_name"))
        # self._session = _aws_config_.setup_session(self._config)
        self._client = self._session.client("secretsmanager")


    @_common_.exception_handler
    def get_secret_value(self, secret_name: str):
        _parameters = {
            "Name": secret_name
        }
        _response = self._client.get_secret_value(**_parameters)

        if _response.get("ResponseMetadata").get("HTTPStatusCode") == 200:
            print(_response)

    def create_secret_value(self, secret_name: str, secret_string: Union[str, Dict], secret_template: str = None):
        _secret_template_map = {
            "rds_credentail_template": ssm_rds_template
        }

        _template_selection_func = _secret_template_map.get(secret_template, ssm_rds_template)
        if _template_selection_func == ssm_default_template and isinstance(secret_string, str):
            _template_parameters = {"secret_string": secret_string}
        else:
            _template_parameters = _template_selection_func(**secret_string)

        _parameters = {
            "Name": secret_name,
            "SecretString": _util_file_.json_dumps(_template_parameters)
        }
        _response = self._client.create_secret(**_parameters)

        if _response.get("ResponseMetadata").get("HTTPStatusCode") == 200:
            _common_.info_logger(f"secret {secret_name} is created successfully")
            return _response
        else:
            return []



