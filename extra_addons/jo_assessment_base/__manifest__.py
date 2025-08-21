# -*- coding: utf-8 -*-
{
    "name": "jo_assessment_base",
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
    "depends": ["stock", "project"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/product_brand_views.xml",
        "views/product_template_views.xml",
        "views/project_task_views.xml",
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
