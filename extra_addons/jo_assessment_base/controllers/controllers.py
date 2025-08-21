# # -*- coding: utf-8 -*-
from typing import List
from odoo import http
from odoo.http import request, Response
import json


class StockAPIController(http.Controller):

    def check_token(self) -> bool:
        token = request.httprequest.headers.get("Authorization")
        expected_token = (
            request.env["ir.config_parameter"].sudo().get_param("jo.stock_api_token")
        )
        if not token or token == expected_token:
            return Response(
                json.dumps({"error": "Unauthorized"}),
                status=401,
                content_type="application/json",
            )
        return True

    def get_all_location_ids(self, location) -> List:
        ids = location.ids
        for child in location.child_ids:
            ids += self.get_all_location_ids(child)
        return ids

    def get_warehouse_location(self, warehouse_code: str) -> List:
        warehouse = (
            request.env["stock.warehouse"]
            .sudo()
            .search([("code", "=", warehouse_code)], limit=1)
        )
        if not warehouse:
            return Response(
                json.dumps({"error": f"Unknown warehouse {warehouse_code}"}),
                status=404,
                content_type="application/json",
            )
        main_location = warehouse.lot_stock_id
        return self.get_all_location_ids(main_location)

    @http.route(
        "/api/v1/stock", type="http", auth="public", methods=["GET"], csrf=False
    )
    def get_stock(self, **kwargs):
        self.check_token()
        skus = kwargs.get("skus")
        warehouse_code = kwargs.get("warehouse")
        if not skus or not warehouse_code:
            return Response(
                json.dumps({"error": "Missing parameters (skus, warehouse)"}),
                status=400,
                content_type="application/json",
            )

        warehouse_location_ids = self.get_warehouse_location(warehouse_code)
        sku_list = skus.split(",")
        Product = request.env["product.product"].sudo()
        stock_quant = request.env["stock.quant"].sudo()

        results = {}
        for sku in sku_list:
            product = Product.search([("default_code", "=", sku)], limit=1)
            if not product:
                results[sku] = {"on_hand": 0.0, "available_to_promise": 0}
            warehouse_quantity = stock_quant.search(
                [
                    ("location_id", "in", warehouse_location_ids),
                    ("product_id", "=", product.id),
                ]
            )
            results[sku] = {
                "on_hand": product.qty_available,
                "available_to_promise": warehouse_quantity.quantity,
            }
        return json.dumps({"warehouse": warehouse_code, "results": results})
