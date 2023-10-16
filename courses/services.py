import stripe

from config.settings import SECRET_KEY

stripe.api_key = SECRET_KEY


def get_payment_link(obj):
    """ Функция формирования ссылки на оплату """

    if obj.price > 0:
        subscription_product = stripe.Product.create(
            name=obj.title,
        )

        subscription_price = stripe.Price.create(
            unit_amount=obj.price * 100,
            currency="rub",
            product=subscription_product['id'],
        )

        payment_link = stripe.PaymentLink.create(
            line_items=[
                {
                    "price": subscription_price.id,
                    "quantity": 1,
                },
            ],
        )

        return payment_link['url']

    else:
        return 'Бесплатно'
