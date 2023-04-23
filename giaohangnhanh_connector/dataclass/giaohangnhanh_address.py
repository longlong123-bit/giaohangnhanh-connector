from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Sequence, Tuple
from odoo.addons.api_connect_instances.dataclass.dictionary_io import InputDict, OutputDict


class KEY_INPUT_DICT_COMMON(Enum):
    IS_ENABLE: str = 'IsEnable'


class KEY_OUTPUT_DICT_COMMON(Enum):
    IS_ENABLE: str = 'active'


class KEY_INPUT_DICT_PROVINCE(Enum):
    ID: str = 'ProvinceID'
    CODE: str = 'Code'
    NAME: str = 'ProvinceName'


class KEY_OUTPUT_DICT_PROVINCE(Enum):
    ID: str = 'pid'
    CODE: str = 'code'
    NAME: str = 'name'


class KEY_INPUT_DICT_DISTRICT(Enum):
    ID: str = 'DistrictID'
    CODE: str = 'Code'
    NAME: str = 'DistrictName'
    PROVINCE_ID: str = 'ProvinceID'


class KEY_OUTPUT_DICT_DISTRICT(Enum):
    ID: str = 'did'
    CODE: str = 'code'
    NAME: str = 'name'
    PROVINCE_ID: str = 'pid'


class KEY_INPUT_DICT_WARD(Enum):
    NAME: str = 'WardName'
    CODE: str = 'WardCode'
    DISTRICT_ID: str = 'DistrictID'


class KEY_OUTPUT_DICT_WARD(Enum):
    NAME: str = 'name'
    CODE: str = 'code'
    DISTRICT_ID: str = 'did'


@dataclass(frozen=True)
class Province(InputDict, OutputDict):
    id: int
    code: str
    name: str
    is_enable: int

    @staticmethod
    def parser_dict(data: Dict[str, Any]) -> Sequence[Tuple]:
        result: tuple = (
            data.get(KEY_INPUT_DICT_PROVINCE.ID.value),
            data.get(KEY_INPUT_DICT_PROVINCE.CODE.value),
            data.get(KEY_INPUT_DICT_PROVINCE.NAME.value),
            data.get(KEY_INPUT_DICT_COMMON.IS_ENABLE.value)
        )
        return result

    @staticmethod
    def parser_class(cls, **kwargs) -> Dict[str, Any]:
        payload: dict = {
            KEY_OUTPUT_DICT_PROVINCE.ID.value: cls.id,
            KEY_OUTPUT_DICT_PROVINCE.CODE.value: cls.code,
            KEY_OUTPUT_DICT_PROVINCE.NAME.value: cls.name,
            KEY_OUTPUT_DICT_COMMON.IS_ENABLE.value: True if cls.is_enable == 1 else False,
        }
        return payload


@dataclass(frozen=True)
class District(InputDict, OutputDict):
    id: int
    code: str
    name: str
    pid: int
    is_enable: bool

    @staticmethod
    def parser_dict(data: Dict[str, Any]) -> Sequence[Tuple]:
        result: tuple = (
            data.get(KEY_INPUT_DICT_DISTRICT.ID.value),
            data.get(KEY_INPUT_DICT_DISTRICT.CODE.value),
            data.get(KEY_INPUT_DICT_DISTRICT.NAME.value),
            data.get(KEY_INPUT_DICT_DISTRICT.PROVINCE_ID.value),
            data.get(KEY_INPUT_DICT_COMMON.IS_ENABLE.value)
        )
        return result

    @staticmethod
    def parser_class(cls, **kwargs) -> Dict[str, Any]:
        payload: dict = {
            KEY_OUTPUT_DICT_DISTRICT.ID.value: cls.id,
            KEY_OUTPUT_DICT_DISTRICT.CODE.value: cls.code,
            KEY_OUTPUT_DICT_DISTRICT.NAME.value: cls.name,
            KEY_OUTPUT_DICT_COMMON.IS_ENABLE.value: True if cls.is_enable == 1 else False,
            KEY_OUTPUT_DICT_DISTRICT.PROVINCE_ID.value: kwargs.get(KEY_OUTPUT_DICT_DISTRICT.PROVINCE_ID.value)
        }
        return payload


@dataclass(frozen=True)
class Ward(InputDict, OutputDict):
    code: str
    name: str
    did: int
    is_enable: bool

    @staticmethod
    def parser_dict(data: Dict[str, Any]) -> Sequence[Tuple]:
        result: tuple = (
            data.get(KEY_INPUT_DICT_WARD.CODE.value),
            data.get(KEY_INPUT_DICT_WARD.NAME.value),
            data.get(KEY_INPUT_DICT_WARD.DISTRICT_ID.value),
            data.get(KEY_INPUT_DICT_COMMON.IS_ENABLE.value)
        )
        return result

    @staticmethod
    def parser_class(cls, **kwargs) -> Dict[str, Any]:
        payload: dict = {
            KEY_OUTPUT_DICT_WARD.CODE.value: cls.code,
            KEY_OUTPUT_DICT_WARD.NAME.value: cls.name,
            KEY_OUTPUT_DICT_WARD.DISTRICT_ID.value: kwargs.get(KEY_OUTPUT_DICT_WARD.DISTRICT_ID.value),
            KEY_OUTPUT_DICT_COMMON.IS_ENABLE.value: True if cls.is_enable == 1 else False
        }
        return payload
