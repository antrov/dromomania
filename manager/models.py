from peewee import *

DATABASE = 'tweepee.db'

database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class OfferGroup(BaseModel):
    offer_url = CharField()
    title = CharField()
    params = CharField(null=True)
    rating = CharField(null=True)
    tag = CharField(null=True)


class Offer(BaseModel):
    image_hash = CharField(primary_key=True)
    """Perceptual hash of image data"""
    image_url = CharField(index=True)
    """URL of image"""
    group = ForeignKeyField(OfferGroup, backref='offers')


def init_db():
    with database:
        database.create_tables([Offer, OfferGroup])
