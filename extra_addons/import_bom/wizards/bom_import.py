# -*- coding: utf-8 -*-

import base64
import csv
import logging

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools import ustr

from ..datamodels.datamodel import BomData, BomType, DataCol, MaterialProduct

_logger = logging.getLogger(__name__)


PRODUCT_CODE = "default_code"


class BomImport(models.TransientModel):
    _name = "bom.import"
    _description = "Import Bom wizard"

    name = fields.Char(string="name")
    bom_type = fields.Selection(
        [("mtp", "Manufacture This Product"), ("kit", "Kit")],
        String="BOM Type",
        Required=True,
        default="mtp",
        helf="Type of Bill of Materials",
    )
    file = fields.Binary(String="Upload File", Required=True, help="File to Import")

    def action_import_bom(self):
        """function for importing bom through csv or Excel file"""
        if self.file:
            try:
                file = base64.b64decode(self.file)
                file_string = file.decode("utf-8")
                file_string.split("\n")
            except Exception as err:
                raise UserError(_("Please choose the correct file!", err)) from err
            for rec in self:
                file = str(base64.decodebytes(rec.file).decode("utf-8"))
                reader = csv.reader(file.splitlines())
                next(reader)
                last_bom_id = False
                rec_count = 0
                try:
                    for line in reader:
                        bom_data = BomData()
                        bom_line_dict = MaterialProduct()
                        if line[DataCol.FINISHED_PROUCT]:
                            rec_count += 1
                            product = self.env["product.template"].search(
                                [("name", "=", line[DataCol.FINISHED_PROUCT])], limit=1
                            )
                            bom_data.product_tmpl_id = product.id
                            bom_data.code = line[DataCol.REF]
                            if line[DataCol.PRODUCT_VARIANT]:
                                variant = self.env["product.product"].search(
                                    [
                                        (
                                            PRODUCT_CODE,
                                            "=",
                                            line[DataCol.PRODUCT_VARIANT],
                                        )
                                    ],
                                    limit=1,
                                )
                                bom_data.product_id = variant.id
                                if line[DataCol.FINISHED_UOM]:
                                    uom = self.env["uom.uom"].search(
                                        [("name", "=", line[DataCol.FINISHED_UOM])],
                                        limit=1,
                                    )
                                    bom_data.product_uom_id = uom.id
                                else:
                                    bom_data.product_uom_id = variant.uom_id
                            if line[DataCol.QUANTITY]:
                                bom_data.product_qty = line[DataCol.QUANTITY]

                            if rec.bom_type == "mtp":
                                bom_data.type = BomType.MRP.value
                            else:
                                bom_data.type = BomType.KIT.value

                            bom_bom = rec.env["mrp.bom"].create(bom_data.model_dump())
                            last_bom_id = bom_bom.id
                        if line[DataCol.MATERIAL_PRODUCT]:
                            variant = self.env["product.product"].search(
                                [(PRODUCT_CODE, "=", line[DataCol.MATERIAL_PRODUCT])],
                                limit=1,
                            )
                            bom_line_dict.product_id = variant.id
                            bom_line_dict.bom_id = last_bom_id
                            if line[DataCol.MATERIAL_QTY]:
                                bom_line_dict.product_qty = line[DataCol.MATERIAL_QTY]

                            if line[DataCol.MATERIAL_UOM]:
                                uom = self.env["uom.uom"].search(
                                    [("name", "=", line[DataCol.MATERIAL_UOM])], limit=1
                                )
                                bom_line_dict.product_uom_id = uom.id
                            else:
                                bom_line_dict.product_uom_id = product.uom_id
                            self.env["mrp.bom.line"].create(bom_line_dict.model_dump())
                    return rec.success_message(rec_count)
                except Exception as e:
                    raise UserError(
                        _(
                            "The CSV file you provided "
                            "does not match our required format" + ustr(e)
                        )
                    ) from e

    def success_message(self, rec_count):
        """function for displaying success message"""
        message_id = self.env["success.message"].create(
            {"message": str(rec_count) + " Records imported successfully"}
        )
        return {
            "name": "Message",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "success.message",
            "res_id": message_id.id,
            "target": "new",
        }
