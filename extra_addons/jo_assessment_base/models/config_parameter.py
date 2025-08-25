# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    jo_default_brand_prefix = fields.Char(
            string="Default Brand Prefix",
            config_parameter="jo.default_brand_prefix",
            default="BR-"
        )
