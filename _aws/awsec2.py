import base64
import random
import time
from inspect import currentframe
from typing import List, Dict, Union, Tuple
from logging import Logger as Log
from botocore.exceptions import ClientError
from _meta import _meta as _meta_
from _config import config as _config_
from _common import _common as _common_
from _aws import awsclient_config as _aws_config_
from _util import _util_common as _util_
from pprint import pprint


class AwsApiAWSEC2(metaclass=_meta_.Meta):
    def __init__(self, config: _config_.AwsApiConfigSingleton = None, logger: Log = None):
        self._config = config if config else _config_.AwsApiConfigSingleton()

        self._session = _aws_config_.setup_session_by_profile(self._config.config.get("aws_profile_name"), self._config.config.get("aws_region_name")) if \
            self._config.config.get("aws_profile_name") and self._config.config.get("aws_region_name") else _aws_config_.setup_session(self._config)
        self._client = self._session.client("ec2")

    @_common_.exception_handler
    def describe_instance(self,
                          instance_ids: Union[str, List],
                          tag_column: str = None,
                          logger: Log = None,
                          *args,
                          **kwargs) -> Dict:

        if isinstance(instance_ids, str):
            instance_ids = [instance_ids]

        _parameters = {"InstanceIds": instance_ids}
        _response = self._client.describe_instances(**_parameters)

        if _response.get("ResponseMetadata").get("HTTPStatusCode") != 200:
            icommon.error_logger(currentframe().f_code.co_name,
                                 f"not able to retrieve object",
                                 logger=logger,
                                 mode="error",
                                 ignore_flag=False)
        else:
            return _response

    @_common_.get_aws_resource("NextToken")
    def describe_instances(self,
                           filtering_field: Union[str, List] = None,
                           tag_column: str = None,
                           logger: Log = None,
                           *args,
                           **kwargs) -> Dict:

        if isinstance(filtering_field, str):
            filtering_field = [filtering_field]

        def get_fields(record: Dict) -> Dict:
            if not filtering_field: return record
            _dict = {}
            for _each_field in filtering_field:
                if n := record.get(_each_field):
                    _dict[_each_field] = n
            return _dict

        def tag_formatter(tags: List) -> Dict:
            return {_each_record.get("Key"): _each_record.get("Value") for _each_record in tags} if len(tags) > 0 else {}

        _next_token = kwargs.get("next_t", {})
        _parameters = _next_token
        if _parameters:
            _response = self._client.describe_instances(**_parameters)
        else:
            _response = self._client.describe_instances()

        if _response.get("ResponseMetadata").get("HTTPStatusCode") == 200:
            return {"result": [{**get_fields(_each_inst), **{"Name": tag_formatter(_each_inst.get("Tags")).get("Name")}} for _each_record in _response.get("Reservations", []) for
                               _each_inst in _each_record.get("Instances", [])] if tag_column else [get_fields(_each_inst) for _each_record in _response.get("Reservations", []) for
                               _each_inst in _each_record.get("Instances", [])],
                    "next_t": _response.get("NextToken")
                    }
        else:
            return {"result": [],
                    "next_t": ""
                    }

    @_common_.exception_handler
    def describe_instance_attribute(self,
                                    instance_id: str,
                                    attribute_name: str,
                                    logger: Log = None,
                                    *args,
                                    **kwargs) -> Union[Dict, str]:
        _parameters = {"InstanceId": instance_id, "Attribute": attribute_name}
        _response = self._client.describe_instance_attribute(**_parameters)
        if _response.get("ResponseMetadata").get("HTTPStatusCode") != 200:
            _common_.error_logger(currentframe().f_code.co_name,
                                 f"not able to retrieve object",
                                 logger=logger,
                                 mode="error",
                                 ignore_flag=False)
        else:
            if attribute_name == "userData":
                return base64.b64decode(_response.get("UserData", {}).get("Value")).decode("UTF-8")
            else:
                return _response





        # if _response.get("ResponseMetadata").get("HTTPStatusCode") == 200:
        #     return {"result": [_each_instance for _each_instance in _response.get("Reservations", {}).get("Instances", [])
        #                        ],
        #             "next_t": _response.get("NextToken")
        #             }
        # else:
        #     return {"result": [],
        #             "next_t": ""
        #             }




