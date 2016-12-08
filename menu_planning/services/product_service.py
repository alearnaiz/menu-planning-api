from menu_planning.models import Product
from menu_planning import db


class ProductService:

    def get_by_id(self, id):
        return Product.query.filter_by(id=id).first()

    def get_all(self):
        return Product.query.all()

    def delete_all(self):
        Product.query.delete()
        db.session.commit()

    def create(self, product):
        db.session.add(product)
        db.session.commit()
        return product

    def create(self, name, status, quantity=None):
        product = Product(name=name, status=status, quantity=quantity)
        db.session.add(product)
        db.session.commit()
        return product

    def update(self, id, name, status, quantity=None):
        product = self.get_by_id(id)
        product.name = name
        product.status = status
        product.quantity = quantity
        db.session.add(product)
        db.session.commit()
        return product

