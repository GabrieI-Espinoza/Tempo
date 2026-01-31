from enum import Enum


# Category labels for events
class CategoryLabel(str, Enum):
    WORK = "Work"
    FAMILY = "Family"
    SOCIAL = "Social"
    FITNESS = "Fitness"
    HIGH_PRIORITY = "High Priority"
    OTHER = "Other"


# Color codes associated with each category
class ColorCode(str, Enum):
    WORK_COLOR = "#3A86FF"
    FAMILY_COLOR = "#8338EC"
    SOCIAL_COLOR = "#FF006E"
    FITNESS_COLOR = "#000000"
    HIGH_PRIORITY_COLOR = "#D00000"
    OTHER_COLOR = "#C5C5C5"


# Mapping from CategoryLabel to ColorCode
CATEGORY_COLOR = {
    CategoryLabel.WORK: ColorCode.WORK_COLOR,
    CategoryLabel.FAMILY: ColorCode.FAMILY_COLOR,
    CategoryLabel.SOCIAL: ColorCode.SOCIAL_COLOR,
    CategoryLabel.FITNESS: ColorCode.FITNESS_COLOR,
    CategoryLabel.HIGH_PRIORITY: ColorCode.HIGH_PRIORITY_COLOR,
    CategoryLabel.OTHER: ColorCode.OTHER_COLOR,
}
