from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Sequence, Tuple
from odoo.addons.api_connect_instances.dataclass.dictionary_io import InputDict, OutputDict


class KEY_INPUT_DICT_STORE(Enum):
    ID: str = '_id'
    NAME: str = 'name'
    PHONE: str = 'phone'
    ADDRESS: str = 'address'
    WARD_CODE: str = 'ward_code'
    DISTRICT_ID: str = 'district_id'
    CLIENT_ID: str = 'client_id'
    VERSION_NO: str = 'version_no'
    STATUS: str = 'status'


class KEY_OUTPUT_DICT_STORE(Enum):
    CID: str = 'cid'
    NAME: str = 'name'
    PHONE: str = 'phone'
    ADDRESS: str = 'address'
    PID: str = 'pid'
    DID: str = 'did'
    WID: str = 'wid'
    CLID: str = 'clid'
    VERSION_NO: str = 'version_no'
    ACTIVE: str = 'active'


@dataclass(frozen=True)
class Store(InputDict, OutputDict):
    id: int
    name: str
    phone: str
    address: str
    ward_code: str
    district_id: int
    client_id: int
    version_no: str
    status: int

    @staticmethod
    def parser_dict(data: Dict[str, Any]) -> Sequence[Tuple]:
        result: tuple = (
            data.get(KEY_INPUT_DICT_STORE.ID.value),
            data.get(KEY_INPUT_DICT_STORE.NAME.value),
            data.get(KEY_INPUT_DICT_STORE.PHONE.value),
            data.get(KEY_INPUT_DICT_STORE.ADDRESS.value),
            data.get(KEY_INPUT_DICT_STORE.WARD_CODE.value),
            data.get(KEY_INPUT_DICT_STORE.DISTRICT_ID.value),
            data.get(KEY_INPUT_DICT_STORE.CLIENT_ID.value),
            data.get(KEY_INPUT_DICT_STORE.VERSION_NO.value),
            data.get(KEY_INPUT_DICT_STORE.STATUS.value)
        )
        return result

    @staticmethod
    def parser_class(cls, **kwargs) -> Dict[str, Any]:
        payload: dict = {
            KEY_OUTPUT_DICT_STORE.CID.value: cls.id,
            KEY_OUTPUT_DICT_STORE.NAME.value: cls.name,
            KEY_OUTPUT_DICT_STORE.PHONE.value: cls.phone,
            KEY_OUTPUT_DICT_STORE.ADDRESS.value: cls.address,
            KEY_OUTPUT_DICT_STORE.PID.value: kwargs.get(KEY_OUTPUT_DICT_STORE.PID.value),
            KEY_OUTPUT_DICT_STORE.DID.value: kwargs.get(KEY_OUTPUT_DICT_STORE.DID.value),
            KEY_OUTPUT_DICT_STORE.WID.value: kwargs.get(KEY_OUTPUT_DICT_STORE.WID.value),
            KEY_OUTPUT_DICT_STORE.CLID.value: cls.client_id,
            KEY_OUTPUT_DICT_STORE.VERSION_NO.value: cls.version_no,
            KEY_OUTPUT_DICT_STORE.ACTIVE.value: True if cls.status == 1 else False
        }
        return payload
