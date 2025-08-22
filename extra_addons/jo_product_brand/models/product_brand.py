from odoo import api, fields, models


class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "Product Brand"
    _rec_name = "name"

    name = fields.Char(string="Brand Name", required=True)
    code = fields.Char(string="Code", required=True)

    _sql_constraints = [("name_uniq", "unique(code)", "Code already exists.")]
