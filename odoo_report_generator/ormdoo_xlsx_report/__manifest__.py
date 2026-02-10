{
    'name': "XLSX Report Generator",
    'summary': """Generate your Report with Excel template""",
    'description': """Simple module to generate report with Excel template""",
    'author': "Olivier Remacle",
    'website': "https://ormdoo.com",
    'images': ["static/description/banner.png"],
    'category': 'Technical',
    'version': '19.0.0.4',
    'application': True,
    'installable': True,
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/xlsx_report_config_view.xml',
        'views/ir_action_report_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ormdoo_xlsx_report/static/src/js/report/action_manager_report.esm.js'
        ]
    },
    'license': 'LGPL-3',
    'external_dependencies': {
        'python': ['xlsxtpl']
    }
    
}
