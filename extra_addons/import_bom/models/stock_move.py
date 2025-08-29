from odoo import _, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    request_order_mo = fields.Boolean(
        "Request MO",
        default=False,
        help="Requsto production goods is not enought goods.",
    )
    mo_picking_type_id = fields.Many2one(
        "stock.picking.type",
        string="MO Picking Type",
        domain="[('code', '=', 'mrp_operation')]",
    )

    def request_mo(self):
        bom = self.env["mrp.bom"].search(
            [("product_id", "=", self.product_id.id)], limit=1
        )
        if not bom:
            raise UserError(
                _(
                    "The product (%s) does not have BOM, Please check product BOM in the Manufacturing.",
                    self.product_id.name,
                )
            )
        if self.request_order_mo:
            raise UserError(
                _(
                    "The product (%s) already request generated MO order, Please check in the Manufacturing Orders.",
                    self.product_id.name,
                )
            )
        if not self.mo_picking_type_id:
            raise UserError(
                _(
                    "Please select the manufacturing operation warehouse for the (%s) product.",
                    self.product_id.name,
                )
            )
        context = {"default_picking_type_id": self.mo_picking_type_id.id}
        self.env["mrp.production"].with_context(context).create_mo(
            product_id=self.product_id.id,
            quantity=self.product_uom_qty,
            ref=self.picking_id.origin,
        )
        self.request_order_mo = True
