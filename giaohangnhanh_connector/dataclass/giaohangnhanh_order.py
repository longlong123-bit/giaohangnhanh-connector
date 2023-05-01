from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Sequence, Tuple, List
from odoo.addons.api_connect_instances.dataclass.dictionary_io import InputDict, OutputDict


class KEY_INPUT_DICT_ORDER(Enum):
    ORDER_CODE: str = 'order_code'
    SORT_CODE: str = 'sort_code'
    TOTAL_FEE: str = 'total_fee'
    TRANS_TYPE: str = 'trans_type'
    EXPECTED_DELIVERY_TIME: str = 'expected_delivery_time'


class KEY_OUTPUT_DICT_ORDER(Enum):
    DELIVERY_ORDER_ID: str = 'delivery_order_id'
    CARRIER_TRACKING_REF: str = 'carrier_tracking_ref'
    TOTAL_FEE: str = 'total_fee'
    TRANS_TYPE: str = 'trans_type'
    EXPECTED_DELIVERY_TIME: str = 'expected_delivery_time'
    STATE: str = 'state'
    SORT_CODE: str = 'sort_code'
    NOTE: str = 'note'
    CARRIER_ID: str = 'carrier_id'
    RECEIVER_ID: str = 'receiver_id'
    SENDER_ID: str = 'sender_id'
    HEIGHT: str = 'height'
    WIDTH: str = 'width'
    WEIGHT: str = 'weight'
    LENGTH: str = 'length'
    SERVICE_ID: str = 'service_id'
    PAYMENT_TYPE_ID: str = 'payment_type_id'
    REQUIRED_NOTE_ID: str = 'required_note_id'
    COD_AMOUNT: str = 'cod_amount'
    INSURANCE_VALUE: str = 'insurance_value'
    CLIENT_ORDER_CODE: str = 'client_order_code'
    COUPON: str = 'coupon'
    ITEM_IDS: str = 'item_ids'


class KEY_OUTPUT_DICT_PRODUCT(Enum):
    NAME: str = 'name'
    QUANTITY: str = 'quantity'
    PRICE: str = 'price'
    LENGTH: str = 'length'
    WIDTH: str = 'width'
    HEIGHT: str = 'height'
    WEIGHT: str = 'weight'
    PRODUCT_ID: str = 'product_id'


class KEY_OUTPUT_SHIPMENT(Enum):
    SHOP_ID: str = 'shop_id'
    TO_NAME: str = 'to_name'
    TO_PHONE: str = 'to_phone'
    TO_ADDRESS: str = 'to_address'
    TO_WARD_NAME: str = 'to_ward_name'
    TO_DISTRICT_NAME: str = 'to_district_name'
    TO_PROVINCE_NAME: str = 'to_province_name'
    WEIGHT: str = 'weight'
    LENGTH: str = 'length'
    WIDTH: str = 'width'
    HEIGHT: str = 'height'
    SERVICE_ID: str = 'service_id'
    SERVICE_TYPE_ID: str = 'service_type_id'
    PAYMENT_TYPE_ID: str = 'payment_type_id'
    INSURANCE_VALUE: str = 'insurance_value'
    CLIENT_ORDER_CODE: str = 'client_order_code'
    COUPON: str = 'coupon'
    NOTE: str = 'note'
    REQUIRED_NOTE: str = 'required_note'
    ITEMS: str = 'items'


class KEY_OUTPUT_ORDER_LINE(Enum):
    PRODUCT_ID: str = 'product_id'
    NAME: str = 'name'
    PRODUCT_UOM_QTY: str = 'product_uom_qty'
    PRICE_UNIT: str = 'price_unit'
    PRICE_SUBTOTAL: str = 'price_subtotal'
    PRICE_TOTAL: str = 'price_total'
    SEQUENCE: str = 'sequence'
    ORDER_ID: str = 'order_id'
    IS_DELIVERY: str = 'is_delivery'


@dataclass(frozen=True)
class Order(InputDict, OutputDict):
    order_code: str
    sort_code: str
    total_fee: int
    trans_type: str
    expected_delivery_time: str

    @staticmethod
    def parser_dict(data: Dict[str, Any]) -> Sequence[Tuple]:
        result: tuple = (
            data.get(KEY_INPUT_DICT_ORDER.ORDER_CODE.value),
            data.get(KEY_INPUT_DICT_ORDER.SORT_CODE.value),
            data.get(KEY_INPUT_DICT_ORDER.TOTAL_FEE.value),
            data.get(KEY_INPUT_DICT_ORDER.TRANS_TYPE.value),
            data.get(KEY_INPUT_DICT_ORDER.EXPECTED_DELIVERY_TIME.value)
        )
        return result

    @staticmethod
    def _get_shipment_items(cls) -> List[Tuple[int, int, Dict[str, Any]]]:
        items = [(0, 0, {
            KEY_OUTPUT_DICT_PRODUCT.NAME.value: item.product_id.name,
            KEY_OUTPUT_DICT_PRODUCT.QUANTITY.value: int(item.quantity),
            KEY_OUTPUT_DICT_PRODUCT.PRICE.value: int(item.price),
            KEY_OUTPUT_DICT_PRODUCT.WEIGHT.value: int(item.weight),
            KEY_OUTPUT_DICT_PRODUCT.PRODUCT_ID.value: item.product_id.id
        }) for item in cls.item_ids]
        return items

    @staticmethod
    def parser_class_order_shipment(cls, external_cls) -> Dict[str, Any]:
        payload: dict = {
            KEY_OUTPUT_DICT_ORDER.DELIVERY_ORDER_ID.value: external_cls.deli_order_id.id,
            KEY_OUTPUT_DICT_ORDER.CARRIER_TRACKING_REF.value: cls.order_code,
            KEY_OUTPUT_DICT_ORDER.TOTAL_FEE.value: cls.total_fee,
            KEY_OUTPUT_DICT_ORDER.TRANS_TYPE.value: cls.trans_type,
            KEY_OUTPUT_DICT_ORDER.SORT_CODE.value: cls.sort_code,
            KEY_OUTPUT_DICT_ORDER.EXPECTED_DELIVERY_TIME.value: datetime.strptime(cls.expected_delivery_time,
                                                                                  '%Y-%m-%dT%H:%M:%SZ'),
            KEY_OUTPUT_DICT_ORDER.STATE.value: r'Chờ lấy hàng',
            KEY_OUTPUT_DICT_ORDER.NOTE.value: external_cls.note or '',
            KEY_OUTPUT_DICT_ORDER.RECEIVER_ID.value: external_cls.receiver_id.id,
            KEY_OUTPUT_DICT_ORDER.SENDER_ID.value: external_cls.sender_id.id,
            KEY_OUTPUT_DICT_ORDER.LENGTH.value: external_cls.length,
            KEY_OUTPUT_DICT_ORDER.WIDTH.value: external_cls.width,
            KEY_OUTPUT_DICT_ORDER.HEIGHT.value: external_cls.height,
            KEY_OUTPUT_DICT_ORDER.WEIGHT.value: external_cls.weight,
            KEY_OUTPUT_DICT_ORDER.SERVICE_ID.value: external_cls.service_id.id,
            KEY_OUTPUT_DICT_ORDER.PAYMENT_TYPE_ID.value: external_cls.payment_type_id.id,
            KEY_OUTPUT_DICT_ORDER.REQUIRED_NOTE_ID.value: external_cls.required_note_id.id,
            KEY_OUTPUT_DICT_ORDER.COD_AMOUNT.value: external_cls.cod_amount,
            KEY_OUTPUT_DICT_ORDER.CLIENT_ORDER_CODE.value: external_cls.client_order_code,
            KEY_OUTPUT_DICT_ORDER.INSURANCE_VALUE.value: external_cls.insurance_value,
            KEY_OUTPUT_DICT_ORDER.COUPON.value: external_cls.coupon,
            KEY_OUTPUT_DICT_ORDER.ITEM_IDS.value: Order._get_shipment_items(external_cls)
        }
        return payload

    @staticmethod
    def parser_class_do(cls, **kwargs) -> Dict[str, Any]:
        payload: dict = {
            KEY_OUTPUT_DICT_ORDER.CARRIER_ID.value: kwargs.get(KEY_OUTPUT_DICT_ORDER.CARRIER_ID.value),
            KEY_OUTPUT_DICT_ORDER.CARRIER_TRACKING_REF.value: cls.order_code
        }
        return payload

    @staticmethod
    def parser_class_order_line(cls, total_fee) -> Dict[str, Any]:
        default_quantity = 1.0
        payload: dict = {
            KEY_OUTPUT_ORDER_LINE.PRODUCT_ID.value: cls.carrier_id.product_id.id,
            KEY_OUTPUT_ORDER_LINE.NAME.value: f'{cls.service_id.display_name}',
            KEY_OUTPUT_ORDER_LINE.PRODUCT_UOM_QTY.value: default_quantity,
            KEY_OUTPUT_ORDER_LINE.PRICE_UNIT.value: total_fee,
            KEY_OUTPUT_ORDER_LINE.PRICE_SUBTOTAL.value: total_fee,
            KEY_OUTPUT_ORDER_LINE.PRICE_TOTAL.value: total_fee,
            KEY_OUTPUT_ORDER_LINE.SEQUENCE.value: cls.deli_order_id.sale_id.order_line[-1].sequence + 1,
            KEY_OUTPUT_ORDER_LINE.ORDER_ID.value: cls.deli_order_id.sale_id.order_line[-1].order_id.id,
            KEY_OUTPUT_ORDER_LINE.IS_DELIVERY.value: True
        }
        return payload

    @staticmethod
    def _get_items(cls) -> (List[Dict[str, Any]], int):
        total_price = 0
        items = []
        for item in cls.item_ids:
            total_price += int(item.price)
            obj_item = {
                KEY_OUTPUT_DICT_PRODUCT.NAME.value: item.product_id.name,
                KEY_OUTPUT_DICT_PRODUCT.QUANTITY.value: int(item.quantity),
                KEY_OUTPUT_DICT_PRODUCT.PRICE.value: int(item.price),
                KEY_OUTPUT_DICT_PRODUCT.WEIGHT.value: int(item.weight)
            }
            items.append(obj_item)
        return items, total_price

    @staticmethod
    def parser_class_shipment(cls) -> Dict[str, Any]:
        items, total = Order._get_items(cls)
        payload: dict = {
            KEY_OUTPUT_SHIPMENT.SHOP_ID.value: cls.sender_id.cid,
            KEY_OUTPUT_SHIPMENT.TO_NAME.value: cls.receiver_id.name,
            KEY_OUTPUT_SHIPMENT.TO_PHONE.value: cls.receiver_id.phone,
            KEY_OUTPUT_SHIPMENT.TO_ADDRESS.value: cls.receiver_id.ghn_street,
            KEY_OUTPUT_SHIPMENT.TO_WARD_NAME.value: cls.receiver_id.ghn_ward_id.name,
            KEY_OUTPUT_SHIPMENT.TO_DISTRICT_NAME.value: cls.receiver_id.ghn_district_id.name,
            KEY_OUTPUT_SHIPMENT.TO_PROVINCE_NAME.value: cls.receiver_id.ghn_province_id.name,
            KEY_OUTPUT_SHIPMENT.WEIGHT.value: int(cls.weight),
            KEY_OUTPUT_SHIPMENT.HEIGHT.value: int(cls.height),
            KEY_OUTPUT_SHIPMENT.LENGTH.value: int(cls.length),
            KEY_OUTPUT_SHIPMENT.WIDTH.value: int(cls.width),
            KEY_OUTPUT_SHIPMENT.SERVICE_ID.value: cls.service_id.service_id,
            KEY_OUTPUT_SHIPMENT.SERVICE_TYPE_ID.value: cls.service_id.service_type_id,
            KEY_OUTPUT_SHIPMENT.PAYMENT_TYPE_ID.value: int(cls.payment_type_id.code),
            KEY_OUTPUT_SHIPMENT.NOTE.value: cls.note or '',
            KEY_OUTPUT_SHIPMENT.REQUIRED_NOTE.value: cls.required_note_id.code,
            KEY_OUTPUT_SHIPMENT.INSURANCE_VALUE.value: total,
            KEY_OUTPUT_SHIPMENT.CLIENT_ORDER_CODE.value: cls.deli_order_id.sale_id.name,
            KEY_OUTPUT_SHIPMENT.COUPON.value: cls.coupon or '',
            KEY_OUTPUT_SHIPMENT.ITEMS.value: items
        }
        return payload
