from uuid import UUID

from fastapi import APIRouter, Depends, status, Request

from src.constants.permissions import PERMISSIONS
from src.schemas.auth_history import AuthHistoryInDB
from src.services.auth_history import AuthHistoryService
from src.utils.jwt import check_token_and_role
from src.utils.pagination import Paginator

router = APIRouter(tags=["auth-history"])


@router.get(
    "/{user_id}",
    response_model=list[AuthHistoryInDB],
    status_code=status.HTTP_200_OK,
    summary="Получение истории аутентификаций пользователя",
)
async def get_auth_history(
    request: Request,
    user_id: UUID,
    service: AuthHistoryService = Depends(AuthHistoryService),
    paginated_params: Paginator = Depends(),
) -> list[AuthHistoryInDB]:
    await check_token_and_role(request, PERMISSIONS["can_read_auth_history"])

    return await service.get_history(
        user_id, paginated_params.page_size, paginated_params.page_number
    )
