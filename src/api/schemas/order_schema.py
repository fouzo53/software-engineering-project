from marshmallow import Schema, fields, validate


class OrderItemSchema(Schema):
    """Schema để validate từng item trong order"""
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    price = fields.Float(load_default=None)  # Optional, will be fetched from product


class CreateOrderSchema(Schema):
    """Schema để validate input khi tạo order"""
    items = fields.List(fields.Nested(OrderItemSchema), required=True, validate=validate.Length(min=1))
    customer_id = fields.Int(required=True)
    payment_method = fields.Str(validate=validate.OneOf(['CASH', 'DEBT']), load_default='CASH')
    total_amount = fields.Float(load_default=None)  # Optional, will be calculated
