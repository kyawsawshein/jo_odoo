from odoo import models, fields, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    request_order_mo = fields.Boolean("Request MO", default=False)

    def request_mo(self):
        bom = self.env["mrp.bom"].search([("product_id", "=", self.product_id.id)], limit=1)
        if not bom:
            raise UserError(_("The product (%s) does not have BOM, Please check product BOM in the Manufacturing.", self.product_id.name))
        if self.request_order_mo:
            raise UserError(_("The product (%s) already request generated MO order, Please check in the Manufacturing Orders.", self.product_id.name))
        self.env["mrp.production"].create_mo(
            product_id=self.product_id.id,
            quantity=self.product_uom_qty,
            ref=self.picking_id.origin,
        )
        self.request_order_mo = True
