from odoo import models, fields, api
from datetime import datetime

import logging


_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    stage_started_on = fields.Datetime(
        string="Stage Started On", readonly=True, copy=False
    )
    completed_on = fields.Datetime(string="Completed On", readonly=True, copy=False)

    @api.onchange("stage_id")
    def _onchange_stage_id(self):
        for task in self:
            if task.stage_id:
                task.stage_started_on = fields.Datetime.now()

    def write(self, vals):
        res = super().write(vals)
        if "stage_id" in vals:
            done_stages = self.env["project.task.type"].search([("name", "=", "Done")])
            for task in self:
                if task.stage_id in done_stages and not task.completed_on:
                    task.completed_on = fields.Datetime.now()

        return res
