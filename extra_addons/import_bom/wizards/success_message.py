# -*- coding: utf-8 -*-
from odoo import models, fields


class SuccessMessage(models.TransientModel):
    """model for adding warning message"""

    _name = "success.message"
    _description = "Show Message"

    message = fields.Text("Success", required=True)

    def action_close(self):
        """function for close button"""
        return {"type": "ir.actions.act_window_close"}
