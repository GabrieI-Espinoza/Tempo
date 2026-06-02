from app.categories.categories import CategoryLabel, CATEGORY_COLOR


def get_categories() -> list[dict]:
    """Return the event categories exposed by the API."""
    return [
        {
            "key": label.name,
            "label": label.value,
            "color_code": CATEGORY_COLOR[label],
        }
        for label in CategoryLabel
    ]
