from flask_app.config.mysqlconnection import connectToMySQL

from datetime import date

from flask_app.models.pantry import Pantry


class History:
    schema_name = "budgeats_schema"
    def __init__(self, data):
        self.id = data["id"]        
        self.pantry_id = data["pantry_id"]
        self.user_id = data["user_id"]
        self.use_date = data["use_date"]
        self.quantity_used = data["quantity_used"]
        self.use_type = data["use_type"]
        self.total_cost = data["total_cost"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.ingredient = []

    @classmethod
    def use_ingredient(cls, data):
        query = "INSERT INTO pantry (ingredient_name, type, measure_type, quantity, total_cost, cost_per_unit, user_id) VALUES (%(ingredient_name)s, %(type)s, %(measure_type)s, %(quantity)s, %(total_cost)s, %(cost_per_unit)s, %(user_id)s);"

        result = connectToMySQL(cls.schema_name).query_db(query, data)

        return result

    @classmethod
    def get_daily_history(cls, data):
        
        query = "SELECT * from history join pantry on pantry_id = pantry.id where pantry.user_id = %(user_id)s AND use_date = %(end_date)s ORDER BY use_date DESC;"

        records = connectToMySQL(cls.schema_name).query_db(query, data)

        daily_history = []
        daily_total = 0
        for record in records:
            daily_total += float(record["total_cost"])
            history = History(record)
            
            ingredient_data = {
                "id": record["pantry.id"],
                "ingredient_name": record["ingredient_name"],
                "type": record["type"],
                "measure_type": record["measure_type"],
                "quantity": record["quantity"],
                "created_at": record["pantry.created_at"],
                "updated_at": record["pantry.updated_at"],
                "cost_per_unit": record["cost_per_unit"],
                "total_cost": record["pantry.total_cost"],
                "user_id": record["pantry.user_id"]           
            }

            history.ingredient = Pantry(ingredient_data)

            daily_history.append(history)

        data = [{"daily_total": daily_total}, daily_history]

        return data

    @classmethod
    def get_weekly_history(cls, data):
        
        query = "SELECT * from history join pantry on pantry_id = pantry.id where pantry.user_id = %(user_id)s AND use_date BETWEEN %(start_date)s AND %(end_date)s ORDER BY use_date DESC;"

        records = connectToMySQL(cls.schema_name).query_db(query, data)

        weekly_history = []
        weekly_total = 0
        for record in records:
            weekly_total += float(record["total_cost"])
            history = History(record)
            
            ingredient_data = {
                "id": record["pantry.id"],
                "ingredient_name": record["ingredient_name"],
                "type": record["type"],
                "measure_type": record["measure_type"],
                "quantity": record["quantity"],
                "created_at": record["pantry.created_at"],
                "updated_at": record["pantry.updated_at"],
                "cost_per_unit": record["cost_per_unit"],
                "total_cost": record["pantry.total_cost"],
                "user_id": record["pantry.user_id"]           
            }

            history.ingredient = Pantry(ingredient_data)

            weekly_history.append(history)

        data = [{"weekly_total": weekly_total}, weekly_history]

        return data

