from odoo import api, fields, models


class Product(models.Model):
    _inherit = "product.product"

    brand_id = fields.Many2one("product.brand", string="Product Brand", index=True)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    brand_id = fields.Many2one("product.brand", string="Product Brand", index=True)
    low_stock_threshold = fields.Float(
        string="Low Stock Threshold",
        default=0.0,
        help="If on-hand quantity is below this value, an alert will be triggered.",
    )

    def post_message_to_task(self, low_stock_products: int):
        purchasing_task = self.env["project.task"].search(
            [("name", "=", "Purchasing")], limit=1
        )
        if purchasing_task:
            body_lines = [
                f"{p.display_name}: {p.qty_available} (Threshold {p.low_stock_threshold or p.reordering_min_qty})"
                for p in low_stock_products
            ]
            summary = "".join(body_lines)
            purchasing_task.message_post(body=f"Daily Low Stock Report: {summary}")

    @api.model
    def _cron_low_stock_alert(self):
        products = self.env["product.product"].search(
            [("low_stock_threshold", ">", 0.0)]
        )
        low_stock_products = products.filtered(
            lambda p: p.qty_available < (p.low_stock_threshold or p.reordering_min_qty)
        )

        if not low_stock_products:
            return

        for product in low_stock_products:
            product.message_post(
                body=f"Low Stock Alert: On hand = {product.qty_available}, "
                f"Threshold = {product.low_stock_threshold or product.reordering_min_qty}"
            )
        self.post_message_to_task(low_stock_products)
