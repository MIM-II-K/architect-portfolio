import math
from typing import Any


def paginate(
    items: list[Any],
    page: int,
    page_size: int,
) -> tuple[list[Any], dict[str, int]]:
    total = len(items)

    total_pages = (
        math.ceil(total / page_size)
        if total
        else 0
    )

    start = (page - 1) * page_size
    end = start + page_size

    return (
        items[start:end],
        {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
        },
    )