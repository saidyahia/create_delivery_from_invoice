# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Create Delivery Order  From Customer Invoice and Auto Validate it',
    'version': '16.0.0.1.0',
    'category': 'Stock',
    'summary': 'Create Delivery Order  From Customer Invoice and Auto Validate it',
    'description': """Create Delivery Order  From Customer Invoice and Auto Validate it""",
    'author': "Said YAHIA",
    'website': "https://www.linkedin.com/in/said-yahia-a3a64261",
    'support': "syahia1111@gmail.com",

    'depends': ['stock_account','account'],
    'data': [
        'views/account_move_views.xml',
    ],
    'images': ['static/description/thumbnail.jpeg'],
    'demo': [],
    'installable': True,
    'auto_install': True,
    'price': 15,
    'currency': 'USD',
    'license': "AGPL-3",


}
