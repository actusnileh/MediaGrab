from pydantic import BaseModel


class HelpItem(BaseModel):
    name: str
    description: list[str]


class HelpResponse(BaseModel):
    help_items: list[HelpItem]
