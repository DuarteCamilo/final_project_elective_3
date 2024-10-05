from schemas.user_group_schema import UserGroup
from database import UserGroupModel
from fastapi import APIRouter, Body, HTTPException

user_group_route = APIRouter()

@user_group_route.post("/")
async def create_user_group(user_group: UserGroup = Body(...)):
    """Add a user to a group."""
    UserGroupModel.create(user_id=user_group.user_id, group_id=user_group.group_id)
    return {"message": "User added to group successfully"}

@user_group_route.get("/")
async def read_all_user_groups():
    """Retrieve a list of all user-group relationships."""
    user_groups = UserGroupModel.select().dicts()
    return list(user_groups)

@user_group_route.get("/{user_group_id}")
async def read_user_group(user_group_id: int):
    """Retrieve a specific user-group relationship by its ID."""
    try:
        user_group = UserGroupModel.get(UserGroupModel.id == user_group_id)
        return user_group
    except Exception as exc:
        raise HTTPException(status_code=404, detail="User-group relationship not found") from exc

@user_group_route.put("/{user_group_id}")
async def update_user_group(user_group_id: int, user_group: UserGroup = Body(...)):
    """Update an existing user-group relationship."""
    try:
        existing_user_group = UserGroupModel.get(UserGroupModel.id == user_group_id)
        existing_user_group.user_id = user_group.user_id
        existing_user_group.group_id = user_group.group_id
        existing_user_group.save()
        return {"message": "User-group relationship updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="User-group relationship not found") from exc

@user_group_route.delete("/{user_group_id}")
async def delete_user_group(user_group_id: int):
    """Delete a user-group relationship by its ID."""
    rows_deleted = UserGroupModel.delete().where(UserGroupModel.id == user_group_id).execute()
    if rows_deleted:
        return {"message": "User removed from group successfully"}
    raise HTTPException(status_code=404, detail="User-group relationship not found")
