{
    'name': "Docx Report Generator",
    'summary': """Generate your Report with DOCX template""",
    'description': """Simple module to generate report with DOCX template""",
    'author': "Olivier Remacle",
    'website': "https://ormdoo.com",
    'images': ["static/description/banner.png"],
    'category': 'Technical',
    'version': '19.0.1.1.2',

    'license': 'LGPL-3',
    'application': True,    
    'installable': True,

    'depends': ['base', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_config_data.xml',
        'views/docx_report_config_view.xml',
        'views/ir_action_report_view.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            'ormdoo_docx_report/static/src/js/report/action_manager_report.esm.js'
        ]
    },

    'external_dependencies': {
        'python': ['docxtpl', 'docxcompose', 'htmldocx'],
    }
    
}
