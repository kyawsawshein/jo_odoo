# -*- coding: utf-8 -*-
{
    "name": "jo_assessment_base",
    "summary": "Short (1 phrase/line) summary of the module's purpose",
    "description": """
Long description of module's purpose
    """,
    "author": "Zervi",
    "website": "https://www.zervi.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Project",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base","project"],
    # always loaded
    "data": [
        "security/security_views.xml",
        # "security/ir.model.access.csv",
        "views/project_task_views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        # 'demo/demo.xml',
    ],
}
