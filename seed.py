"""Seed file to make sample data for db."""
from models import Pet, db
from app import app

# Create all tables
db.drop_all()
db.create_all()


# Make a bunch of pets


p1 = Pet(name='Fluffy', species='dog',
         photo_url='https://d17fnq9dkz9hgj.cloudfront.net/breed-uploads/2022/03/teddybear-dog-breeds.jpeg?bust=1646780646')
p2 = Pet(name='Sparky', species='dog',
         photo_url='https://www.collinsdictionary.com/images/full/dog_230497594.jpg', age=3)
p3 = Pet(name='Garfield', species='cat',
         photo_url='https://i.pinimg.com/originals/11/4a/f1/114af14908e548d41a3bec3e40d58caa.jpg', age=2, available=False)
p4 = Pet(name='Whiskers', species='cat', notes='Still has not arrived')


db.session.add_all([p1, p2, p3, p4])

db.session.commit()
