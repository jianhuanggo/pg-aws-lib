from collections import defaultdict
from inspect import currentframe
from _common import _common as _common_
from typing import Dict
from _util import _util_file as _util_file_


class AwsApiConfigSingleton:

    def __new__(cls, config_loc: str = ".".join(__file__.split(".")[:-1]) + ".yaml"):
        if not hasattr(cls, "instance"):
            cls.config = defaultdict(str)
            cls.instance = super(AwsApiConfigSingleton, cls).__new__(cls)
            """

            Args:
                config_loc: default configuration file location
            """
            try:
                for _name, _val in _util_file_.yaml_load(config_loc).items():
                    cls.config[_name] = _val
            except Exception as err:
                _common_.error_logger(currentframe().f_code.co_name,
                                     err,
                                     logger=None,
                                     mode="error",
                                     ignore_flag=False)

        return cls.instance


class AwsApiConfig:
    def __init__(self, config_loc: str = ".".join(__file__.split(".")[:-1]) + ".yaml"):
        """ automatically parse the content of _config.yaml into a variable

        Args:
            config_loc: default configuration file location
        """
        try:
            self._config = defaultdict(str)
            for _name, _val in _util_file_.yaml_load(config_loc).items():
                self._config[_name] = _val
        except Exception as err:
            _common_.error_logger(currentframe().f_code.co_name,
                                 err,
                                 logger=None,
                                 mode="error",
                                 ignore_flag=False)

    def add(self, configuration: Dict):
        """ add name value pair as configuration

        Args:
            configuration: contains a map of configuration in name value pair

        Returns:

        """
        try:
            for _name, _val in configuration.items():
                self._config[_name] = _val
        except Exception as err:
            _common_.error_logger(currentframe().f_code.co_name,
                                 err,
                                 logger=None,
                                 mode="error",
                                 ignore_flag=False)

    @property
    def config(self):
        return self._config
