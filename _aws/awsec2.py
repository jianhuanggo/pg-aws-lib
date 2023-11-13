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
from time import sleep
from _util import _util_common as _util_
from pprint import pprint

__WAIT_TIME__ = 5

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
            _common_.error_logger(currentframe().f_code.co_name,
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

    @_common_.exception_handler
    def describe_images(self,
                        image_id: Union[List, str]):

        if isinstance(image_id, str):
            image_id = [image_id]
        _parameters = {
            "ImageIds": image_id
        }

        _response = self._client.describe_images(**_parameters)
        if _response.get("ResponseMetadata").get("HTTPStatusCode") == 200:
            return [_each_image for _each_image in _response.get("Images")]
        else:
            _common_.info_logger(_response)
            return []

    @_common_.exception_handler
    def create_image(self,
                     instance_id: str,
                     image_name: str):

        _parameters = {
            "InstanceId": instance_id,
            "Name": image_name
        }
        _response = self._client.create_image(**_parameters)

        if _response.get("ResponseMetadata").get("HTTPStatusCode") == 200:
            _image_id = _response.get("ImageId")
            while True:
                if n := self.describe_images(_image_id):
                    if n[0].get("State") != "pending":
                        if n[0].get("State") == "available":
                            _common_.info_logger("image creation is successful")
                        else:
                            _common_.info_logger("image creation is not successful")
                        break
                sleep(__WAIT_TIME__)
                _common_.info_logger("image creation is in process, please wait...")







    """
    response = client.create_image(
    BlockDeviceMappings=[
        {
            'DeviceName': 'string',
            'VirtualName': 'string',
            'Ebs': {
                'DeleteOnTermination': True|False,
                'Iops': 123,
                'SnapshotId': 'string',
                'VolumeSize': 123,
                'VolumeType': 'standard'|'io1'|'io2'|'gp2'|'sc1'|'st1'|'gp3',
                'KmsKeyId': 'string',
                'Throughput': 123,
                'OutpostArn': 'string',
                'Encrypted': True|False
            },
            'NoDevice': 'string'
        },
    ],
    Description='string',
    DryRun=True|False,
    InstanceId='string',
    Name='string',
    NoReboot=True|False,
    TagSpecifications=[
        {
            'ResourceType': 'capacity-reservation'|'client-vpn-endpoint'|'customer-gateway'|'carrier-gateway'|'coip-pool'|'dedicated-host'|'dhcp-options'|'egress-only-internet-gateway'|'elastic-ip'|'elastic-gpu'|'export-image-task'|'export-instance-task'|'fleet'|'fpga-image'|'host-reservation'|'image'|'import-image-task'|'import-snapshot-task'|'instance'|'instance-event-window'|'internet-gateway'|'ipam'|'ipam-pool'|'ipam-scope'|'ipv4pool-ec2'|'ipv6pool-ec2'|'key-pair'|'launch-template'|'local-gateway'|'local-gateway-route-table'|'local-gateway-virtual-interface'|'local-gateway-virtual-interface-group'|'local-gateway-route-table-vpc-association'|'local-gateway-route-table-virtual-interface-group-association'|'natgateway'|'network-acl'|'network-interface'|'network-insights-analysis'|'network-insights-path'|'network-insights-access-scope'|'network-insights-access-scope-analysis'|'placement-group'|'prefix-list'|'replace-root-volume-task'|'reserved-instances'|'route-table'|'security-group'|'security-group-rule'|'snapshot'|'spot-fleet-request'|'spot-instances-request'|'subnet'|'subnet-cidr-reservation'|'traffic-mirror-filter'|'traffic-mirror-session'|'traffic-mirror-target'|'transit-gateway'|'transit-gateway-attachment'|'transit-gateway-connect-peer'|'transit-gateway-multicast-domain'|'transit-gateway-policy-table'|'transit-gateway-route-table'|'transit-gateway-route-table-announcement'|'volume'|'vpc'|'vpc-endpoint'|'vpc-endpoint-connection'|'vpc-endpoint-service'|'vpc-endpoint-service-permission'|'vpc-peering-connection'|'vpn-connection'|'vpn-gateway'|'vpc-flow-log'|'capacity-reservation-fleet'|'traffic-mirror-filter-rule'|'vpc-endpoint-connection-device-type'|'verified-access-instance'|'verified-access-group'|'verified-access-endpoint'|'verified-access-policy'|'verified-access-trust-provider'|'vpn-connection-device-type'|'vpc-block-public-access-exclusion'|'ipam-resource-discovery'|'ipam-resource-discovery-association'|'instance-connect-endpoint',
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        },
    ]
)
    
    
    """



        # if _response.get("ResponseMetadata").get("HTTPStatusCode") == 200:
        #     return {"result": [_each_instance for _each_instance in _response.get("Reservations", {}).get("Instances", [])
        #                        ],
        #             "next_t": _response.get("NextToken")
        #             }
        # else:
        #     return {"result": [],
        #             "next_t": ""
        #             }




