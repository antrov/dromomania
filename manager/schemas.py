from marshmallow import Schema, fields, post_load, validates, ValidationError

class OfferSchema(Schema):
    image_url = fields.Url()
    offer_url = fields.Url(required=True)
    title = fields.Str()
    tag = fields.Str()
