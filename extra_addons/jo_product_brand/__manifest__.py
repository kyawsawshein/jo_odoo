# -*- coding: utf-8 -*-
{
    "name": "jo_product_brand",
    "summary": "Short (1 phrase/line) summary of the module's purpose",
    "description": """
Long description of module's purpose
    """,
    "author": "Zervi",
    "company": "Zervi",
    "website": "https://www.zerviglobal.com",
    "category": "Product",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["stock"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "security/security_views.xml",
        "views/res_user_views.xml",
        "views/product_brand_views.xml",
        "views/product_template_views.xml",
        "data/ir_cron_view.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        # 'demo/demo.xml',
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
