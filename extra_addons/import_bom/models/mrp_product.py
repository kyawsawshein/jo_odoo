# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


SIZE_BACK_ORDER_NUMERING = 3


class MrpProduction(models.Model):
    _inherit = "mrp.production"

