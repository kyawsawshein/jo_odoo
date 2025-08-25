# # -*- coding: utf-8 -*-
import json
import logging
from functools import wraps
from typing import List, Optional

from pydantic import BaseModel

from odoo import http
from odoo.exceptions import AccessDenied
from odoo.http import Response, request

_logger = logging.getLogger(__name__)

BEARER = "Bearer "


class ProductOnHand(BaseModel):
    product: Optional[str] = ""
    on_hand: Optional[float] = 0.0
    available_to_promise: Optional[float] = 0.0


class ResponseResult(BaseModel):
    warehouse: Optional[str] = ""
    results: list[ProductOnHand] = None


def check_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.httprequest.headers.get("Authorization")
        if token.startswith(BEARER):
            token = token[len(BEARER) :]
        expected = (
            request.env["ir.config_parameter"].sudo().get_param("jo.stock_api_token")
        )
        if not token or token != expected:
            raise AccessDenied("Invalid or missing token.")
        return func(*args, **kwargs)

    return wrapper


class StockAPIController(http.Controller):

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
    @check_token
    def get_stock(self, **kwargs):
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

        results = []
        for sku in sku_list:
            product_onhand = ProductOnHand()
            product = Product.search([("default_code", "=", sku)], limit=1)
            if not product:
                # results[sku] = {"on_hand": 0.0, "available_to_promise": 0}
                product_onhand.product = sku
                results.append(product_onhand)
                continue
            warehouse_quantity = stock_quant.search(
                [
                    ("location_id", "in", warehouse_location_ids),
                    ("product_id", "=", product.id),
                ]
            )
            product_onhand.product = sku
            product_onhand.on_hand = product.qty_available
            product_onhand.available_to_promise = warehouse_quantity.quantity
            results.append(product_onhand)
            _logger.info(product_onhand)

        return json.dumps(
            ResponseResult(warehouse=warehouse_code, results=results).model_dump()
        )
