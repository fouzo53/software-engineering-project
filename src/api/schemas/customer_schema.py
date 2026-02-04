from marshmallow import Schema, fields, validate, pre_load, post_dump


class CustomerSchema(Schema):
    """Schema cho Customer"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    phone = fields.Str(required=True, validate=validate.Length(min=10, max=20))
    address = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    debt_amount = fields.Float(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @post_dump
    def format_phone_param(self, data, **kwargs):
        if 'phone' in data and data['phone']:
            phone = str(data['phone'])
            if phone.startswith('0'):
                data['phone'] = '+84' + phone[1:]
        return data


class CustomerCreateSchema(Schema):
    """Schema cho tạo Customer mới"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    phone = fields.Str(required=True, validate=validate.Length(min=10, max=20))
    address = fields.Str(required=True, validate=validate.Length(min=1, max=255))

    @pre_load
    def format_phone(self, data, **kwargs):
        if 'phone' in data and data['phone']:
            phone = str(data['phone']).strip()
            if phone.startswith('0'):
                data['phone'] = '+84' + phone[1:]
        return data


class CustomerUpdateSchema(Schema):
    """Schema cho cập nhật Customer"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    phone = fields.Str(required=True, validate=validate.Length(min=10, max=20))
    address = fields.Str(required=True, validate=validate.Length(min=1, max=255))

    @pre_load
    def format_phone(self, data, **kwargs):
        if 'phone' in data and data['phone']:
            phone = str(data['phone']).strip()
            if phone.startswith('0'):
                data['phone'] = '+84' + phone[1:]
        return data


class DebtTransactionSchema(Schema):
    """Schema cho DebtTransaction"""
    id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    transaction_type = fields.Str(required=True, validate=validate.OneOf(['debt', 'payment']))
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    note = fields.Str(load_default=None)
    created_at = fields.DateTime(dump_only=True)


class DebtTransactionCreateSchema(Schema):
    """Schema cho tạo giao dịch nợ/trả nợ"""
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    note = fields.Str(load_default=None)
