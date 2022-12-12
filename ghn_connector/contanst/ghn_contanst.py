class Const:
    BASE_CODE = 'ghn_base_url'
    DELIVERY_CARRIER_CODE = 'ghn'


class Message:
    BASE_MSG = 'Giao Hang Nhanh base url not found.'
    MSG_NOT_CARRIER = 'Giao Hang Nhanh delivery carrier not found.'
    MSG_ACTION_SUCCESS = 'Everything seems properly works well!'


class FuncName:
    SyncProvinces = 'SyncProvinces'
    SyncDistricts = 'SyncDistricts'
    SyncWards = 'SyncWards'
    SyncStores = 'SyncStores'
    GenerateStore = 'GenerateStore'
    GetPickShift = 'GetPickShift'
    GetServices = 'GetServices'
    CalculateFee = 'CalculateFee'


class Method:
    POST = 'POST'
    GET = 'GET'
