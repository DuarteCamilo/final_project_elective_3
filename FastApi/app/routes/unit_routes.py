from schemas.unit_schema import Unit
from database import UnitModel
from fastapi import APIRouter, Body, HTTPException

unit_route = APIRouter()

@unit_route.post("/")
async def create_unit(unit: Unit = Body(...)):
    """Create a new unit."""
    UnitModel.create(name=unit.name)
    return {"message": "Unit created successfully"}

@unit_route.get("/")
async def read_all_units():
    """Retrieve a list of all units."""
    units = UnitModel.select().dicts()
    return list(units)

@unit_route.get("/{unit_id}")
async def read_unit(unit_id: int):
    """Retrieve a specific unit by its ID."""
    try:
        unit = UnitModel.get(UnitModel.id == unit_id)
        return unit
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Unit not found") from exc

@unit_route.put("/{unit_id}")
async def update_unit(unit_id: int, unit: Unit = Body(...)):
    """Update an existing unit."""
    try:
        existing_unit = UnitModel.get(UnitModel.id == unit_id)
        existing_unit.name = unit.name
        existing_unit.save()
        return {"message": "Unit updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Unit not found") from exc

@unit_route.delete("/{unit_id}")
async def delete_unit(unit_id: int):
    """Delete a unit by its ID."""
    rows_deleted = UnitModel.delete().where(UnitModel.id == unit_id).execute()
    if rows_deleted:
        return {"message": "Unit deleted successfully"}
    raise HTTPException(status_code=404, detail="Unit not found")
