"""
database.py

This module sets up the database connection using Peewee ORM and defines 
the data models for the cooking application. It loads environment variables for 
database credentials using dotenv and creates models for recipes, ingredients, 
menus, shopping lists, and more.
"""

# Standard library imports
import os

# Third-party imports
from dotenv import load_dotenv
from peewee import Model, MySQLDatabase, AutoField, CharField, ForeignKeyField
from peewee import IntegerField, DecimalField, BooleanField, TextField, DateField

# Load environment variables from .env file
load_dotenv()

# Database configuration using MySQL
database = MySQLDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST')
)

# Models

class UserModel(Model):
    """Model representing a user."""
    id = AutoField(primary_key=True)
    username = CharField(max_length=50)
    email = CharField(max_length=100)
    password_hash = CharField(max_length=255)
    profile_picture = CharField(max_length=255, null=True)

    class Meta:
        """Database configuration for UserModel"""
        database = database
        table_name = "users"

class GroupModel(Model):
    """Model representing a user group."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)

    class Meta:
        """Database configuration for GroupModel"""
        database = database
        table_name = "groups"

class UserGroupModel(Model):
    """Model representing a relationship between user and group."""
    user_id = ForeignKeyField(UserModel, backref='groups')
    group_id = ForeignKeyField(GroupModel, backref='users')

    class Meta:
        """Database configuration for UserGroupModel"""
        database = database
        table_name = "user_groups"

class IngredientCategoryModel(Model):
    """Model representing a category for ingredients."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)

    class Meta:
        """Database configuration for IngredientCategoryModel"""
        database = database
        table_name = "ingredient_categories"

class IngredientModel(Model):
    """Model representing an ingredient."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    category_id = ForeignKeyField(IngredientCategoryModel, backref='ingredients')
    unit_id = IntegerField()

    class Meta:
        """Database configuration for IngredientModel"""
        database = database
        table_name = "ingredients"

class RecipeModel(Model):
    """Model representing a recipe."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    description = TextField()
    instructions = TextField()
    preparation_time = IntegerField()  # Time in minutes
    datos_nutricionales = TextField()
    type = CharField(max_length=50)
    difficulty = CharField(max_length=50)
    is_public = BooleanField(default=True)
    user_id = ForeignKeyField(UserModel, backref='recipes')

    class Meta:
        """Database configuration for RecipeModel"""
        database = database
        table_name = "recipes"

class RecipeIngredientModel(Model):
    """Model representing an ingredient in a recipe."""
    recipe_id = ForeignKeyField(RecipeModel, backref='recipe_ingredients')
    ingredient_id = ForeignKeyField(IngredientModel, backref='used_in_recipes')
    quantity = DecimalField(max_digits=5, decimal_places=2)
    unit = CharField(max_length=20)

    class Meta:
        """Database configuration for RecipeIngredientModel"""
        database = database
        table_name = "recipe_ingredients"

class RecipeTypeModel(Model):
    """Model representing a recipe type."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)

    class Meta:
        """Database configuration for RecipeTypeModel"""
        database = database
        table_name = "recipe_types"

class RecipeRecipeTypeModel(Model):
    """Model representing the relationship between a recipe and its type."""
    recipe_id = ForeignKeyField(RecipeModel, backref='recipe_types')
    type_id = ForeignKeyField(RecipeTypeModel, backref='recipes')

    class Meta:
        """Database configuration for RecipeRecipeTypeModel"""
        database = database
        table_name = "recipe_recipe_types"

class FavoriteRecipeModel(Model):
    """Model representing a user's favorite recipe."""
    user_id = ForeignKeyField(UserModel, backref='favorite_recipes')
    recipe_id = ForeignKeyField(RecipeModel, backref='favorited_by')

    class Meta:
        """Database configuration for FavoriteRecipeModel"""
        database = database
        table_name = "favorite_recipes"

class MenuModel(Model):
    """Model representing a menu."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    user_id = ForeignKeyField(UserModel, backref='menus')
    start_date = DateField()
    end_date = DateField()

    class Meta:
        """Database configuration for MenuModel"""
        database = database
        table_name = "menus"

class MenuRecipeModel(Model):
    """Model representing a recipe in a menu."""
    menu_id = ForeignKeyField(MenuModel, backref='menu_recipes')
    recipe_id = ForeignKeyField(RecipeModel, backref='menus')
    meal_time = CharField(max_length=50)
    planned_date = DateField()

    class Meta:
        """Database configuration for MenuRecipeModel"""
        database = database
        table_name = "menu_recipes"

class ShoppingListModel(Model):
    """Model representing a shopping list."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    created_at = DateField()
    user_id = ForeignKeyField(UserModel, backref='shopping_lists')

    class Meta:
        """Database configuration for ShoppingListModel"""
        database = database
        table_name = "shopping_lists"

class ShoppingListItemModel(Model):
    """Model representing an item in a shopping list."""
    shopping_list_id = ForeignKeyField(ShoppingListModel, backref='items')
    ingredient_id = ForeignKeyField(IngredientModel, backref='in_shopping_lists')
    quantity = DecimalField(max_digits=5, decimal_places=2)
    unit = CharField(max_length=20)
    is_purchased = BooleanField(default=False)

    class Meta:
        """Database configuration for ShoppingListItemModel"""
        database = database
        table_name = "shopping_list_items"

class PantryItemModel(Model):
    """Model representing an item in the pantry."""
    id = AutoField(primary_key=True)
    quantity = DecimalField(max_digits=5, decimal_places=2)
    unit = CharField(max_length=20)
    expiry_date = DateField()
    user_id = ForeignKeyField(UserModel, backref='pantry_items')
    ingredient_id = ForeignKeyField(IngredientModel, backref='stored_in_pantries')

    class Meta:
        """Database configuration for PantryItemModel"""
        database = database
        table_name = "pantry_items"

class UnitModel(Model):
    """Model representing a unit of measurement."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=20)

    class Meta:
        """Database configuration for UnitModel"""
        database = database
        table_name = "units"

class NotificationModel(Model):
    """Model representing a notification sent to a user."""
    id = AutoField(primary_key=True)
    user_id = ForeignKeyField(UserModel, backref='notifications')
    message = TextField()
    created_at = DateField()
    is_read = BooleanField(default=False)

    class Meta:
        """Database configuration for NotificationModel"""
        database = database
        table_name = "notifications"

# Connect to the database
database.connect()