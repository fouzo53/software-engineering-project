from marshmallow import Schema, fields, validate


class OwnerSchema(Schema):
    """Schema cho Owner"""
    id = fields.Int(dump_only=True)
    username = fields.Str()
    full_name = fields.Str()
    status = fields.Str()
    subscription = fields.Str()


class SubscriptionUpdateSchema(Schema):
    """Schema cho cập nhật gói cước"""
    subscription = fields.Str(required=True, validate=validate.OneOf(['basic', 'pro']))


class PlatformStatsSchema(Schema):
    """Schema cho thống kê toàn sàn"""
    total_users = fields.Int()
    total_orders_this_month = fields.Int()
    month = fields.Str()
    stats_date = fields.Str()


class ReportConfigSchema(Schema):
    """Schema cho config báo cáo tài chính"""
    # Config có thể chứa bất kỳ trường nào, dạng JSON linh hoạt
    # Ví dụ: report_format, columns, filters, etc.
    class Meta:
        # Allow any additional fields
        additional = ('report_format', 'columns', 'filters', 'footer', 'header')
