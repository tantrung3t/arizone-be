from . import models


def add_rating(star, product_id):
    product = models.Product.objects.get(id=product_id)
    product.average_rating = round((
        (product.average_rating * product.amount_rating) + star)/(product.amount_rating + 1), 1)
    product.amount_rating += 1
    product.save()