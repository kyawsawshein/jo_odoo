from odoo import models
from odoo.exceptions import ValidationError


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        if not self.env.user.has_group(
            "jo_product_brand.group_brand_restricted_manager"
        ):
            prodcut_brand_ids = []
            for move in self.move_ids.filtered(lambda m: m.product_id.brand_id):
                prodcut_brand_ids.append(move.product_id.brand_id.id)

            if prodcut_brand_ids not in self.env.user.brand_ids.ids:
                raise ValidationError("Product brand not allowed this user.")

        return super().button_validate()
