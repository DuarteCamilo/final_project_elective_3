"""
main.py

This is the main entry point for the FastAPI application. It handles the initialization of 
the app, setting up the lifespan context, and registering API routes for recipes, menus, 
ingredients, and other entities related to the cooking application.

The application connects to the database at startup, creates necessary tables if they 
don't exist, and ensures that the database connection is closed properly upon shutdown.
"""
# pylint: disable=E0401
# Standard library imports
from contextlib import asynccontextmanager

# Local imports (from your project)
from helpers.api_key_auth import get_api_key
from database import database as connection
from database import (
    UserModel, GroupModel, UserGroupModel, IngredientModel, IngredientCategoryModel,
    RecipeModel, RecipeIngredientModel, RecipeTypeModel, RecipeRecipeTypeModel, 
    MenuModel, MenuRecipeModel, ShoppingListModel, ShoppingListItemModel,
    PantryItemModel, UnitModel, NotificationModel, FavoriteRecipeModel
)
from routes.recipe_routes import recipe_router
from routes.menu_routes import menu_router
from routes.shopping_list_routes import shopping_list_router
from routes.ingredient_routes import ingredient_router
from routes.notification_routes import notification_router

# Third-party imports
from fastapi import Depends, FastAPI


# Lifespan context manager to handle the lifecycle of the FastAPI app
@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Manages the lifespan of the FastAPI app. It ensures that the database connection 
    is opened at the start of the app's lifecycle and closed when the app shuts down.

    Args:
        _app (FastAPI): The FastAPI instance.

    Yields:
        None
    """
    if connection.is_closed():
        connection.connect()
        connection.create_tables([
            UserModel, GroupModel, UserGroupModel, IngredientModel, IngredientCategoryModel,
            RecipeModel, RecipeIngredientModel, RecipeTypeModel, RecipeRecipeTypeModel, 
            MenuModel, MenuRecipeModel, ShoppingListModel, ShoppingListItemModel,
            PantryItemModel, UnitModel, NotificationModel, FavoriteRecipeModel
        ])

    try:
        yield

    finally:
        if not connection.is_closed():
            connection.close()


# Initialize the FastAPI application with the custom lifespan function
app = FastAPI(lifespan=lifespan)

# API KEY Validation
@app.get("/protected-endpoint")
async def protected_endpoint(api_key: str = Depends(get_api_key)):
    """
    Protected endpoint that requires a valid API key for access.

    This function handles requests to the /protected-endpoint route. 
    It validates the API key provided in the request's security header using the 
    get_api_key function. If the API key is valid, the function grants access 
    to the protected resource.

    Args:
        api_key (str): The API key extracted and validated using the get_api_key dependency.

    Returns:
        dict: A message indicating access to the protected endpoint with the valid API key.
    """
    return {"message": f"Acceso concedido a endpoint protegido con el key {api_key}"}

# Register the recipe-related routes
app.include_router(recipe_router, prefix="/api/recipes",
                   tags=["recipes"], dependencies=[Depends(get_api_key)])

# Register the menu-related routes
app.include_router(menu_router, prefix="/api/menus",
                   tags=["menus"], dependencies=[Depends(get_api_key)])

# Register the shopping list-related routes
app.include_router(shopping_list_router, prefix="/api/shopping-lists",
                   tags=["shopping-lists"], dependencies=[Depends(get_api_key)])

# Register the ingredient-related routes
app.include_router(ingredient_router, prefix="/api/ingredients",
                   tags=["ingredients"], dependencies=[Depends(get_api_key)])

# Register the notification-related routes
app.include_router(notification_router, prefix="/api/notifications",
                   tags=["notifications"], dependencies=[Depends(get_api_key)])