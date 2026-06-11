from decimal import Decimal

def calculate_delivery_cost(total, delivery_type, address_in_ge=False):
    """
    Рассчитывает стоимость доставки.
    
    Параметры:
    - total: сумма заказа (Decimal, int или float)
    - delivery_type: 'pickup', 'delivery_inside', 'delivery_outside'
    - address_in_ge: True, если адрес в ЖК (только для delivery_inside)
    
    Возвращает:
    - стоимость доставки (Decimal)
    """
    if delivery_type == 'pickup':
        return Decimal('0')
    elif delivery_type == 'delivery_inside':
        # Бесплатно при заказе от 1200 руб, иначе 200 руб
        if address_in_ge and total >= Decimal('1200'):
            return Decimal('0')
        else:
            return Decimal('200')
    else:  # delivery_outside
        return Decimal('200')