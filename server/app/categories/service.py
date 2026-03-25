from typing import List
from app.categories.categories import CategoryLabel, CATEGORY_COLOR


# Function to get all categories with their labels and color codes
def get_categories() -> List[dict]:
    return [
        {
            "key": label.name,  # Enum member name as key
            "label": label.value,  # Enum member as label
            "color_code": CATEGORY_COLOR[label],  # Corresponding color code
        }
        # Iterate over all Categories
        for label in CategoryLabel
    ]
