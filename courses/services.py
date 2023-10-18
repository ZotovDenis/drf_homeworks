import stripe

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def get_link(obj):
    if obj.course:
        title = obj.course.title
        description = obj.course.description
    else:
        title = obj.lesson.title
        description = obj.lesson.description

    product = stripe.Product.create(
        name=title,
        description=description
    )
    product_price = stripe.Price.create(
        unit_amount=int(obj.payment_amount) * 100,
        currency='rub',
        product=product['id']
    )

    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/payments/success/?success=true&session_id={CHECKOUT_SESSION_ID}',
        line_items=[
            {
                'price': product_price,
                'quantity': 1
            }
        ],
        mode='payment',
        metadata={
            'payment_id': obj.id
        }
    )
    obj.session_id = session.id
    obj.save()
    return session['url']
