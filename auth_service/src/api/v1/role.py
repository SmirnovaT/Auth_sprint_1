from fastapi import APIRouter, Depends, Request, status

from src.schemas.role import RoleRead
from src.services.roles import RoleService, PERMISSIONS
from src.utils.jwt import check_token_and_role

router = APIRouter(tags=["role"])


@router.post(
    "",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создание новой роли",
    description="Создание новой роли для разграничения прав пользователей",
)
async def role_creating(
        request: Request,
        role_name: str,
        roles_service: RoleService = Depends(RoleService),
) -> RoleRead:
    await check_token_and_role(request, PERMISSIONS["can_perform_roles"])

    created_role = await roles_service.create_role(role_name)

    return created_role
