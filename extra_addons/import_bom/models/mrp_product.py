# -*- coding: utf-8 -*-
import logging
from itertools import groupby
from typing import Dict, List

from odoo import fields, models

from ..datamodels.datamodel import MRP

SIZE_BACK_ORDER_NUMERING = 3

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def get_product_bom(self, product_id: int, quantity: int, mrp_date: List[MRP]):
        bom = self.env["mrp.bom"].search([("product_id", "=", product_id)], limit=1)
        if bom:
            mrp_date.append(
                MRP(
                    product_id=product_id,
                    product_qty=quantity,
                    bom_id=bom.id,
                    product_uom_id=bom.product_uom_id.id,
                )
            )
            for bom_line in bom.bom_line_ids:
                self.get_product_bom(
                    bom_line.product_id.id, bom_line.product_qty * quantity, mrp_date
                )

    def compute_borm(self, product_id: int, quantity: int) -> List:
        mrp_date = []
        self.get_product_bom(
            product_id=product_id, quantity=quantity, mrp_date=mrp_date
        )
        return mrp_date

    def compute_component_bom(self, product_id: int, quantity: int) -> Dict:
        mo_data = {}
        mrp_date = self.compute_borm(product_id=product_id, quantity=quantity)
        for mrp in mrp_date:
            if mo_data.get(mrp.product_id):
                mo_data[mrp.product_id].product_qty += mrp.product_qty
            else:
                mo_data[mrp.product_id] = mrp

        _logger.info("mo data : %s", mo_data)
        return mo_data

    def create_mo(self, product_id: int = 140, quantity: int = 1, ref: str = "SO"):
        product_mo = self.compute_component_bom(
            product_id=product_id, quantity=quantity
        )
        for _, mo in product_mo.items():
            mo.date_start = fields.Date.today()
            mo.date_finished = fields.Date.today()
            mo.user_id = 2
            mo.origin = ref
            self.create(mo.model_dump())


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    product_id = fields.Many2one("product.product", "Product Variant", required=True)
    _sql_constraints = [
        ("prodcut_uniq", "unique(product_id, company_id)", "Code already exists.")
    ]
