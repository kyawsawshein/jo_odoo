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
    request_mo_quantity = fields.Integer()
    visible_mo_request = fields.Boolean(
        compute="_compute_visible_mo_request", default=False
    )

    def _compute_visible_mo_request(self):
        for stock in self:
            stock.visible_mo_request = False
            if stock.picking_id and stock.picking_type_id.code in ("outgoing"):
                stock.visible_mo_request = True

    def check_product_bom(self):
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

    def check_request_mo_quantity(self):
        if not self.request_mo_quantity:
            raise UserError(_("Pleae set the Manufacturing Order quantities."))
        if self.request_mo_quantity > self.product_uom_qty:
            raise UserError(_("Manufacturing order exceeds product uom quantiy."))

    def request_mo(self):
        self.check_product_bom()
        self.check_request_mo_quantity()
        context = {"default_picking_type_id": self.mo_picking_type_id.id}
        self.env["mrp.production"].with_context(context).create_mo(
            product_id=self.product_id.id,
            quantity=self.request_mo_quantity,
            ref=self.picking_id.origin,
        )
        self.request_order_mo = True
