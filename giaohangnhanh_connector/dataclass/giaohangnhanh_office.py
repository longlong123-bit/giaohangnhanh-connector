import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Sequence, Tuple
from odoo.addons.api_connect_instances.dataclass.dictionary_io import InputDict, OutputDict


class KEY_INPUT_DICT_OFFICE(Enum):
    ADDRESS: str = 'address'
    LOCATION_CODE: str = 'locationCode'
    LOCATION_ID: str = 'locationId'
    LOCATION_NAME: str = 'locationName'
    EMAIL: str = 'email'
    LATITUDE: str = 'latitude'
    LONGITUDE: str = 'longitude'
    WARD_NAME: str = 'wardName'
    DISTRICT_NAME: str = 'districtName'
    PROVINCE_NAME: str = 'provinceName'
    IFRAME_MAP: str = 'iframeMap'


class KEY_OUTPUT_DICT_OFFICE(Enum):
    NAME: str = 'name'
    CODE: str = 'code'
    OFFICE_ID: str = 'office_id'
    EMAIL: str = 'email'
    PROVINCE_NAME: str = 'province_name'
    DISTRICT_NAME: str = 'district_name'
    WARD_NAME: str = 'ward_name'
    ADDRESS: str = 'address'
    LATITUDE: str = 'latitude'
    LONGITUDE: str = 'longitude'
    IFRAME_MAP: str = 'iframe_map'


@dataclass(frozen=True)
class Office(InputDict, OutputDict):
    address: str
    location_code: str
    location_id: int
    location_name: str
    email: str
    latitude: float
    longitude: float
    ward_name: str
    district_name: str
    province_name: str
    iframe_map: str

    @staticmethod
    def _change_css_for_iframe_map(iframe_map):
        iframe_map = re.sub(r'width=\d+', 'width=100%', iframe_map)
        return iframe_map

    @staticmethod
    def parser_dict(data: Dict[str, Any]) -> Sequence[Tuple]:
        result: tuple = (
            data.get(KEY_INPUT_DICT_OFFICE.ADDRESS.value),
            data.get(KEY_INPUT_DICT_OFFICE.LOCATION_CODE.value),
            data.get(KEY_INPUT_DICT_OFFICE.LOCATION_ID.value),
            data.get(KEY_INPUT_DICT_OFFICE.LOCATION_NAME.value),
            data.get(KEY_INPUT_DICT_OFFICE.EMAIL.value),
            data.get(KEY_INPUT_DICT_OFFICE.LATITUDE.value),
            data.get(KEY_INPUT_DICT_OFFICE.LONGITUDE.value),
            data.get(KEY_INPUT_DICT_OFFICE.WARD_NAME.value),
            data.get(KEY_INPUT_DICT_OFFICE.DISTRICT_NAME.value),
            data.get(KEY_INPUT_DICT_OFFICE.PROVINCE_NAME.value),
            data.get(KEY_INPUT_DICT_OFFICE.IFRAME_MAP.value)
        )
        return result

    @staticmethod
    def parser_class(cls, **kwargs) -> Dict[str, Any]:
        iframe = Office._change_css_for_iframe_map(cls.iframe_map)
        payload: dict = {
            KEY_OUTPUT_DICT_OFFICE.NAME.value: cls.location_name,
            KEY_OUTPUT_DICT_OFFICE.CODE.value: cls.location_code,
            KEY_OUTPUT_DICT_OFFICE.OFFICE_ID.value: cls.location_id,
            KEY_OUTPUT_DICT_OFFICE.EMAIL.value: cls.email,
            KEY_OUTPUT_DICT_OFFICE.PROVINCE_NAME.value: cls.province_name,
            KEY_OUTPUT_DICT_OFFICE.DISTRICT_NAME.value: cls.district_name,
            KEY_OUTPUT_DICT_OFFICE.WARD_NAME.value: cls.ward_name,
            KEY_OUTPUT_DICT_OFFICE.ADDRESS.value: cls.address,
            KEY_OUTPUT_DICT_OFFICE.LATITUDE.value: cls.latitude,
            KEY_OUTPUT_DICT_OFFICE.LONGITUDE.value: cls.longitude,
            KEY_OUTPUT_DICT_OFFICE.IFRAME_MAP.value: iframe
        }
        return payload
