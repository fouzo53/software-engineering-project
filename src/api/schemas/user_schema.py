from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    """Schema để validate input khi login"""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6))


class RegisterSchema(Schema):
    """Schema để validate input khi register"""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    role = fields.Str(load_default="employee", validate=validate.OneOf(["user", "owner", "admin", "employee"]))


class UserSchema(Schema):
    """Schema để serialize User object"""
    id = fields.Int()
    username = fields.Str()
    role = fields.Str()
    full_name = fields.Str()
    subscription = fields.Str()


class LoginResponseSchema(Schema):
    """Schema để serialize login response"""
    success = fields.Bool()
    message = fields.Str()
    token = fields.Str()
    user = fields.Nested(UserSchema)


class RegisterResponseSchema(Schema):
    """Schema để serialize register response"""
    success = fields.Bool()
    message = fields.Str()
    user = fields.Nested(UserSchema)
