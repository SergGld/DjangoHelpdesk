# -*- coding: utf-8 -*-
from rolepermissions.roles import AbstractUserRole

ROLES = (
    ('user', 'Пользователь'),
    ('staff', 'Обслуживающий'),
    ('admin', 'Администратор'),
    ('chief', 'Шеф'),
)
class Staff(AbstractUserRole):
    name='Staff';
    available_permissions = {
        'answer_ticket': True,
    }
class User(AbstractUserRole):
    name='User';
    available_permissions = {
        'answer_ticket': False,
    }