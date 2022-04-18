from flask_app import app 
from flask_app.config.mysqlconnection import connectToMySQL #don't know why is not MySQLConnection but at least this works
from flask import flash


class Recipes:
    def __init__(self,data): 
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id'] #foreign key
        
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes ( name, description, instructions, date_made, user_id) VALUES ( %(name)s, %(description)s, %(instructions)s, %(date_made)s, %(user_id)s);"
        return connectToMySQL('recipes_schema').query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_schema').query_db(query)
        print(results)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe))
        return recipes
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls(results[0])
    
    
    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s , date_made=%(date_made)s, updated_at=NOW() WHERE id = %(id)s"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query, data)
    
    
