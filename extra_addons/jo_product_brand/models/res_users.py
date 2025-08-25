from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    brand_ids = fields.Many2many(
        "product.brand",
        "user_product_brand_rel",
        "user_id",
        "brand_id",
        string="Allowed Brands",
    )
