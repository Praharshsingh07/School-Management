{
    'name': 'Hotel_Management',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Manage hotel rooms, bookings, and customers',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hotel_room_views.xml',
        'views/hotel_booking_views.xml',
        'views/hotel_customer_views.xml',
        'views/hotel_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto-install': False,
    'license': 'LGPL-3',
}
