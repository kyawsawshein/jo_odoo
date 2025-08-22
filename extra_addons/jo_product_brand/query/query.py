
class SQL:
    get_warehouse_qty = """
        select pt.name,sq.quantity
        FROM stock_quant sq
            INNER JOIN product_product pp ON pp.id=sq.product_id
            INNER JOIN product_template pt ON pt.id=pp.product_tmpl_id
            INNER JOIN stock_location sl ON sl.id=sq.location_id
        WHERE sl.usage = 'internal'
        AND pt.default_code IN ('PROD001','PROD002')
        ANd sl.id IN (8,14)
    """
