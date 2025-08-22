# -*- coding: utf-8 -*-
{
    "name": "Import BOM",
    "version": "0.1",
    "category": "Manufacturing",
    "summary": """Import Bill of materials using CSV.""",
    "description": "Import Bill of materials using CSV.",
    "author": "Zervi",
    "company": "Zervi",
    "website": "https://www.zerviglobal.com",
    "depends": ["mrp"],
    "data": {
        "security/ir.model.access.csv",
        "report/mrp_report_views.xml",
        "report/mrp_report.xml",
        "views/bom_import_menu_view.xml",
        "views/mrp_product_views.xml",
        "wizards/bom_import_view.xml",
        "wizards/success_message_view.xml",
    },
    "assets": {
        "web.assets_backend": [],
    },
    "installable": True,
    "auto_install": False,
    "application": False,
}
