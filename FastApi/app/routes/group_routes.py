from schemas.group_schema import Group
from database import GroupModel
from fastapi import APIRouter, Body, HTTPException

group_route = APIRouter()

@group_route.post("/")
async def create_group(group: Group = Body(...)):
    """Create a new user group."""
    GroupModel.create(name=group.name)
    return {"message": "Group created successfully"}

@group_route.get("/")
async def read_all_groups():
    """Retrieve a list of all groups."""
    groups = GroupModel.select().dicts()
    return list(groups)

@group_route.get("/{group_id}")
async def read_group(group_id: int):
    """Retrieve a specific group by its ID."""
    try:
        group = GroupModel.get(GroupModel.id == group_id)
        return group
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Group not found") from exc

@group_route.put("/{group_id}")
async def update_group(group_id: int, group: Group = Body(...)):
    """Update an existing group."""
    try:
        existing_group = GroupModel.get(GroupModel.id == group_id)
        existing_group.name = group.name
        existing_group.save()
        return {"message": "Group updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Group not found") from exc

@group_route.delete("/{group_id}")
async def delete_group(group_id: int):
    """Delete a group by its ID."""
    rows_deleted = GroupModel.delete().where(GroupModel.id == group_id).execute()
    if rows_deleted:
        return {"message": "Group deleted successfully"}
    raise HTTPException(status_code=404, detail="Group not found")
