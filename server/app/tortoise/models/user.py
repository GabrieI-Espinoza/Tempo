import uuid
from tortoise.models import Model
from tortoise import fields


class User(Model):
    user_id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    email = fields.CharField(max_length=100, unique=True)
    password_hash = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=50, null=False)
    last_name = fields.CharField(max_length=50, null=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"User<{self.user_id}> {self.email}"
