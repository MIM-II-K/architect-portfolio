from enum import Enum

class ProjectSort(str, Enum):
    newest = "newest"
    oldest = "oldest"
    title_asc = "title_asc"
    title_desc = "title_desc"
    order = "order"