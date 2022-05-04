from flask_app.config.mysqlconnection import connectToMySQL


class Pantry:
    schema_name = "budgeats_schema"
    def __init__(self, data):
        self.id = data["id"]        
        self.ingredient_name = data["ingredient_name"]
        self.type = data["type"]
        self.measure_type = data["measure_type"]
        self.quantity = data["quantity"]
        self.total_cost = data["total_cost"]
        self.cost_per_unit = data["cost_per_unit"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def add_ingredient(cls, data):
        query = "INSERT INTO pantry (ingredient_name, type, measure_type, quantity, total_cost, cost_per_unit, user_id) VALUES (%(ingredient_name)s, %(type)s, %(measure_type)s, %(quantity)s, %(total_cost)s, %(cost_per_unit)s, %(user_id)s);"

        result = connectToMySQL(cls.schema_name).query_db(query, data)

        return result

    @classmethod
    def edit_ingredient(cls, data):
        query = "UPDATE pantry SET ingredient_name = %(ingredient_name)s, type = %(type)s, measure_type = %(measure_type)s, quantity = %(quantity)s, total_cost = %(total_cost)s, cost_per_unit = %(cost_per_unit)s WHERE id = %(id)s;"

        result = connectToMySQL(cls.schema_name).query_db(query, data)

        return result

    @classmethod 
    def delete_ingredient(cls, data):
        query = "DELETE FROM pantry where id = %(id)s;"

        result = connectToMySQL(cls.schema_name).query_db(query, data)

        return 

    @classmethod
    def get_all_ingredients(cls, data):
        
        query = "SELECT * FROM pantry where user_id = %(user_id)s AND quantity > 0 ORDER BY ingredient_name asc;"
        
        records = connectToMySQL(cls.schema_name).query_db(query, data)

        all_ingredients = []
    
        for record in records:
            ingredient = Pantry(record)
            
        
            all_ingredients.append(ingredient)

        return all_ingredients

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM pantry WHERE id = %(id)s;"

        result = connectToMySQL(cls.schema_name).query_db(query,data)

        return cls(result[0])

    @classmethod
    def use_ingredient(cls, data):        

        query = "INSERT INTO history (pantry_id, user_id, use_date, quantity_used, use_type, total_cost) VALUES (%(pantry_id)s, %(user_id)s, %(use_date)s, %(quantity_used)s, %(use_type)s, %(total_cost)s);"

        result = connectToMySQL(cls.schema_name).query_db(query,data)
        
        query = "UPDATE pantry SET quantity = %(quantity)s WHERE id = %(pantry_id)s;"

        result = connectToMySQL(cls.schema_name).query_db(query,data)

        return


