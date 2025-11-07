from tortoise import models, fields

class User(models.Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField()
    name = fields.CharField(max_length=200)
    phone_number = fields.CharField(max_length=25)

    is_premium = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class QuarterSettings(models.Model):
    id = fields.IntField(pk=True)
    current_quarter = fields.IntField(default=1)  # 1, 2, 3, 4
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class UserQuarterSubscription(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='quarter_subscriptions')
    quarter_number = fields.IntField()  # 1, 2, 3, 4
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'quarter_number')

class PresentationFiles(models.Model):
    id = fields.IntField(pk=True)
    file_id = fields.CharField(max_length=256)

    lesson_name = fields.CharField(max_length=256)
    lesson_number = fields.IntField()
    part_number = fields.IntField()
    class_number = fields.IntField()
    file_lang = fields.CharField(max_length=10)
    created_at = fields.DatetimeField(auto_now_add=True)