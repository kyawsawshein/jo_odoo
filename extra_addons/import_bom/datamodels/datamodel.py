from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class BomType(Enum):
    MRP = "normal"
    KIT = "phantom"


class DataCol(Enum):
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
    material: List[MaterialProduct] = None
