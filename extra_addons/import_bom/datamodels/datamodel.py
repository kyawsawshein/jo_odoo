from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class BomType(Enum):
    MRP = "normal"
    KIT = "phantom"


class DataCol:
    REF = 0
    FINISHED_PROUCT = 1
    PRODUCT_VARIANT = 2
    QUANTITY = 3
    FINISHED_UOM = 4
    MATERIAL_PRODUCT = 5
    MATERIAL_QTY = 6
    MATERIAL_UOM = 7


class MaterialProduct(BaseModel):
    bom_id: Optional[int] = 0
    product_id: Optional[str] = ""
    product_qty: int = 1
    product_uom_id: Optional[str] = ""


class BomData(BaseModel):
    product_tmpl_id: Optional[str] = ""
    code: Optional[str] = ""
    product_id: Optional[str] = ""
    product_uom_id: Optional[int] = 0
    product_qty: int = 1
    type: Optional[str] = ""


class RawMove(BaseModel):
    product_id: int
    product_uom: int
    location_id: int
    locaton_dest_id: int
    product_qty: int
    product_uom_qty: int
    quantity: int
    raw_material_prodcution_id: int
    workorder_id: int


class MRP(BaseModel):
    product_id: int
    product_qty: int
    bom_id: int
    product_uom_id: Optional[int] = None
    date_start: Optional[datetime] = None
    date_finished: Optional[datetime] = None
    user_id: Optional[int] = None
    origin: Optional[str] = None
