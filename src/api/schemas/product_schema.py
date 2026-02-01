from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    """Schema để validate và serialize Product"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    cost_price = fields.Float(load_default=0.0, validate=validate.Range(min=0))
    stock = fields.Int(required=True, validate=validate.Range(min=0))
    category_id = fields.Int(required=True)
    image_url = fields.Str(load_default=None)


class ProductImportSchema(Schema):
    """Schema cho nhập hàng vào kho"""
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    cost_price = fields.Float(required=True, validate=validate.Range(min=0))
