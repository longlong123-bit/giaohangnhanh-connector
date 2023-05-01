class Const:
    INSTANCE_CODE = 'giaohangnhanh'
    REQUIRE_NOTE_DEFAULT = 'CHOXEMHANGKHONGTHU'
    PAYMENT_TYPE_DEFAULT = '1'
    MAXIMUM_DEPTH_SIZE_PACKER = 150
    MAXIMUM_WEIGHT_SIZE_PACKER = 30000
    MAXIMUM_WIDTH_SIZE_PACKER = 150
    MAXIMUM_HEIGHT_SIZE_PACKER = 150
    MAXIMUM_INSURANCE_VALUE = 5000000
    MAXIMUM_COD_VALUE = 10000000
    TRACKING_LINK = 'https://donhang.ghn.vn/?order_code={bl_code}'
    URL_PRINT_A5 = '{host}/a5/public-api/printA5?token={token}'
    URL_PRINT_80x80 = '{host}/a5/public-api/print80x80?token={token}'
    URL_PRINT_52x70 = '{host}/a5/public-api/print52x70?token={token}'


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
    SyncPostOffices = 'SyncPostOffices'
    CreateOrder = 'CreateOrder'
    CancelOrder = 'CancelOrder'
    PrintOrder = 'PrintOrder'


class Method:
    POST = 'POST'
    GET = 'GET'
