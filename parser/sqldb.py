from sqlalchemy import create_engine, Column, Integer, Float, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

class Database:
    def __init__(self, db_path):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add(self, id, name, price):
        new_product = Product(id=id, name=name, price=price)
        self.session.add(new_product)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)
            return 1

    def update_price(self, id, new_price):
        try:
            product = self.session.query(Product).filter(Product.id == id).first()
            if product:
                product.price = new_price
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)
            return 1

    def get_price_from_id(self, id):
        product = self.session.query(Product).filter(Product.id == id).first()
        return product.price if product else None

    def get_name_from_id(self, id):
        product = self.session.query(Product).filter(Product.id == id).first()
        return product.name if product else None

    def get_price_from_name(self, name):
        products = self.session.query(Product).filter(Product.name == name).all()
        return [product.price for product in products] if products else None

    def delete_product_by_id(self, id):
        try:
            # Находим продукт по ID
            product = self.session.query(Product).filter(Product.id == id).first()
            if product:
                # Удаляем найденный продукт
                self.session.delete(product)
                self.session.commit()
                return True
            return False  # Если продукт не найден, возвращаем False
        except Exception as e:
            self.session.rollback()
            print(e)
            return False

if __name__ == '__main__':
    db = Database("products.db")
    db.add(4, "dsadas", 215.1)
    print(db.get_price_from_id(4))