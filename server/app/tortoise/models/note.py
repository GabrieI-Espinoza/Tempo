from tortoise.models import Model
from tortoise import fields


class Note(Model):
    note_id = fields.UUIDField(primary_key=True)
    user = fields.ForeignKeyField("models.User", related_name="notes")
    event = fields.ForeignKeyField("models.Event", related_name="notes", null=True)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
