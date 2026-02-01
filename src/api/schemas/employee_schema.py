from marshmallow import Schema, fields, validate


class EmployeeCreateSchema(Schema):
    """Schema cho tạo nhân viên mới"""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=100))
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))


class EmployeeSchema(Schema):
    """Schema cho Employee"""
    id = fields.Int(dump_only=True)
    username = fields.Str()
    full_name = fields.Str()
    role = fields.Str()
    status = fields.Str()


class EmployeeStatusSchema(Schema):
    """Schema cho cập nhật trạng thái nhân viên"""
    status = fields.Str(required=True, validate=validate.OneOf(['active', 'inactive']))
