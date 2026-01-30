from enum import Enum
from tortoise.models import Model
from tortoise import fields


class CategoryLabel(str, Enum):
    WORK = "Work"
    FAMILY = "Family"
    SOCIAL = "Social"
    FITNESS = "Fitness"
    HIGH_PRIORITY = "High Priority"
    OTHER = "Other"


class ColorCode(str, Enum):
    WORK_COLOR = "#3A86FF"
    FAMILY_COLOR = "#8338EC"
    SOCIAL_COLOR = "#FF006E"
    FITNESS_COLOR = "#000000"
    HIGH_PRIORITY_COLOR = "#D00000"
    OTHER_COLOR = "#C5C5C5"


class Category(Model):
    category_id = fields.IntField(pk=True)

    label = fields.CharEnumField(CategoryLabel)
    color_code = fields.CharEnumField(ColorCode)
