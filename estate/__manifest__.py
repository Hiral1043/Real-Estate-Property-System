{
    'name' :"Estate",
    'version' : "18.0.1.0",
    'category': 'Real Estate/Brokerage',
    "summary" : "This is real estate module",
    "website" : 'https://www.estate.com',
    "data" :[
        "security/ir.model.access.csv",
        "security/security.xml",
        "view/estate_property_views.xml",
        "view/estate_property_type_view.xml",
        "view/estate_property_tag_view.xml",
        "view/estate_property_offer_view.xml",
        "view/res_users.xml",
        "view/contact.xml",
        "wizard/sold_property_wizard_view.xml",
        "data/master_data.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
        "view/menu.xml",  # Split the data in multiple files depending on the model
    ],
    "demo": [
        "demo/demo_data.xml",
    ],
    'depends': ['contacts'],
    'license': 'LGPL-3',
    "installable" : True,
    "application" : True


}