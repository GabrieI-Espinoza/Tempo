from tortoise.models import Model
from tortoise import fields


class Event(Model):
    event_id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="events")
    title = fields.CharField(max_length=200)
    description = fields.TextField(null=True)
    location = fields.CharField(max_length=255, null=True)

    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()

    category = fields.ForeignKeyField("models.Category", related_name="events")

    recurring = fields.BooleanField(default=False)
