from fastapi.routing import APIRouter

from fastapi_cache.decorator import cache

from app.schema.help_schema import HelpResponse
from app.services.help_service import HelpService


router = APIRouter(tags=["Help"], prefix="/help")


@router.get(
    "",
    summary="Получить список функций и описание по работе с ними",
    response_model=HelpResponse,
)
@cache(expire=120)
def get_help():
    return HelpService().get_help()
