from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    def request_mo(self):
        self.env['mrp.production'].create_mo(product_id=self.product_id.id, quantity=self.product_uom_qty, ref=self.picking_id.origin)
