from dotenv import load_dotenv
from peewee import *
import os

# Load environment variables
load_dotenv()

# Database configuration using MySQL
database = MySQLDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST')
)

class UserModel(Model):
    id = AutoField(primary_key=True)
    username = CharField(max_length=50)
    email = CharField(max_length=50)
    password_hash = CharField(max_length=100)  # Hash instead of plain password

    class Meta:
        database = database
        table_name = "users"

class GroupModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)

    class Meta:
        database = database
        table_name = "groups"

class IngredientCategoryModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)

    class Meta:
        database = database
        table_name = "ingredient_categories"

class UnitModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)

    class Meta:
        database = database
        table_name = "units"

class IngredientModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    category_id = ForeignKeyField(IngredientCategoryModel, backref='ingredients')
    unit_id = ForeignKeyField(UnitModel, backref='ingredients')

    class Meta:
        database = database
        table_name = "ingredients"

class NotificationModel(Model):
    id = AutoField(primary_key=True)
    user_id = ForeignKeyField(UserModel, backref='notifications')
    message = TextField()
    created_at = DateTimeField()
    is_read = BooleanField()

    class Meta:
        database = database
        table_name = "notifications"

class MenuModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    user_id = ForeignKeyField(UserModel, backref='menus')
    start_date = DateField()
    end_date = DateField()

    class Meta:
        database = database
        table_name = "menus"

# class PantryItem(Model):
#     id = AutoField(primary_key=True)
#     quantity = FloatField()
#     unit = CharField(max_length=50)//haccer lo mismo que esta en las otras tablas ajustandolo
    #lo demas esta bueno es ajustarlo en el main solamente!
#     expiry_date = DateField()
#     user_id = ForeignKeyField(UserModel, backref='pantry_items')
#     ingredient_id = ForeignKeyField(Ingredient, backref='pantry_items')

#     class Meta:
#         database = database
#         table_name = "pantry_items"

class RecipeTypeModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)

    class Meta:
        database = database
        table_name = "recipe_types"

class RecipeModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    description = TextField()
    instructions = TextField()
    preparation_time = IntegerField()
    datosNutricionales = TextField()
    type_id = ForeignKeyField(RecipeTypeModel, backref='recipes')
    difficulty = CharField(max_length=50)
    is_public = BooleanField()
    user_id = ForeignKeyField(UserModel, backref='recipes')

    class Meta:
        database = database
        table_name = "recipes"

class FavoriteRecipeModel(Model):
    id = AutoField(primary_key=True)
    user_id = ForeignKeyField(UserModel, backref='favorite_recipes')
    recipe_id = ForeignKeyField(RecipeModel, backref='favorite_recipes')

    class Meta:
        database = database
        table_name = "favorite_recipes"

class MenuRecipeModel(Model):
    id = AutoField(primary_key=True)
    menu_id = ForeignKeyField(MenuModel, backref='menu_recipes')
    recipe_id = ForeignKeyField(RecipeModel, backref='menu_recipes')
    meal_time = CharField(max_length=50)
    planned_date = DateField()

    class Meta:
        database = database
        table_name = "menu_recipes"

class RecipeRecipeTypeModel(Model):
    id = AutoField(primary_key=True)
    recipe_id = ForeignKeyField(RecipeModel, backref='recipe_recipe_types', on_delete='CASCADE')
    type_id = ForeignKeyField(RecipeTypeModel, backref='recipe_recipe_types', on_delete='CASCADE')

    class Meta:
        database = database
        table_name = "recipe_recipe_types"

class RecipeIngredientModel(Model):
    id = AutoField(primary_key=True)
    recipe_id = ForeignKeyField(RecipeModel, backref='recipe_ingredients')
    ingredient_id = ForeignKeyField(IngredientModel, backref='recipe_ingredients')
    quantity = FloatField()
    unit_id = ForeignKeyField(UnitModel, backref='recipe_ingredients')

    class Meta:
        database = database
        table_name = "recipe_ingredients"

# class ShoppingListModel(Model):
#     id = AutoField(primary_key=True)
#     name = CharField(max_length=50)
#     created_at = DateTimeField()
#     user_id = ForeignKeyField(UserModel, backref='shopping_lists')
        #esta bien hay que agregarlo es ajustar en el main el llamado
#     class Meta:
#         database = database
#         table_name = "shopping_lists"
#

# class ShoppingListItemModel(Model):
#     id = AutoField(primary_key=True)
#     shopping_list_id = IntegerField() /// aqui tiene que hace lo de la forenea como esta abajo 
            #pero con ShoppingList asi
    #shopping_list_id =ForeignKeyField(ShoppingListModel, backref='shopping_list_items')
#     ingredient_id = ForeignKeyField(Ingredient, backref='shopping_list_items')
#     quantity = FloatField()
#     unit = CharField(max_length=50)//lo mismo con unit fijese en cualquier otros que ya esta hecho es acomodarlo
#     is_purchased = BooleanField()
#
#     class Meta:
#         database = database
#         table_name = "shopping_list_items"


class UserGroupModel(Model):
    id = AutoField(primary_key=True)
    user_id = ForeignKeyField(UserModel, backref='user_groups', on_delete='CASCADE')
    group_id = ForeignKeyField(GroupModel, backref='user_groups', on_delete='CASCADE')

    class Meta:
        database = database
        table_name = "user_groups"
