# noinspection PyStatementEffect
{
    'name': "Cash Register",
    'summary': """Keep track balance counts""",
    'description': """Long description of module's purpose""",
    'author': "BenCo",
    'website': "math.mcgill.ca/bsmith",
    'category': 'Cash Management',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/cash_register_view.xml',
        'views/cash_count_view.xml',
        'views/count_generate_view.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}