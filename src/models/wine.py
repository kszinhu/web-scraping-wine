from src.db import db


class WineModel(db.Model):
    __tablename__ = 'wines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)
    image = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(80), nullable=False)

    def __init__(self, name, price, image, country, year, type):
        self.name = name
        self.price = price
        self.image = image
        self.country = country
        self.year = year
        self.type = type

    def __repr__(self, ):
        return f'WineModel(name={self.name}, price={self.price}, image={self.image}, country={self.country}, year={self.year}, type={self.type})'

    def json(self, ):
        return {'name': self.name, 'price': self.price, 'image': self.image, 'country': self.country, 'year': self.year, 'type': self.type}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self, ):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self, ):
        db.session.delete(self)
        db.session.commit()
