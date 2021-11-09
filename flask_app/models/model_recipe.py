from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO recipes ( name, description, instructions, date_made, under_30, user_id, created_at, updated_at ) VALUES ( %(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s, NOW() , NOW() );"
        return connectToMySQL('recipes_schema').query_db( query, data )
    
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('recipes_schema').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under_30=%(under_30)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
        return is_valid