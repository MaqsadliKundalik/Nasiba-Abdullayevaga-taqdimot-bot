from tortoise import models, fields

class User(models.Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField()
    name = fields.CharField(max_length=200)
    phone_number = fields.CharField(max_length=25)

    is_premium = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class PresentationFiles(models.Model):
    id = fields.IntField(pk=True)
    file_id = fields.CharField(max_length=256)

    lesson_name = fields.CharField(max_length=256)
    lesson_number = fields.IntField()
    part_number = fields.IntField()
    class_number = fields.IntField()
    file_lang = fields.CharField(max_length=10)
    created_at = fields.DatetimeField(auto_now_add=True)