from flask_app import app

from flask import render_template, redirect, request, session, flash

from flask_app.models.user import User
from flask_app.models.pantry import Pantry
from flask_app.models.history import History

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from datetime import date
from datetime import timedelta

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/signup/process", methods = ["POST"])
def register_user():
    
    if not User.validate_register(request.form):
        return redirect("/signup")
    
    password_hash = bcrypt.generate_password_hash(request.form["password"])
    
    data = {
        "username": request.form["username"],
        "email": request.form["email"],
        "password": password_hash
    }

    user_id = User.register_user(data)

    session["user_id"] = user_id

    return redirect("/dashboard")



@app.route('/login')
def login():
    return render_template("/login.html")

@app.route('/signup')
def signup():
    return render_template("/signup.html")

@app.route('/dashboard')
def dashboard():

    data = {"user_id": session["user_id"]}

    user = User.get_by_id(data)

    test = ["Monday", "Tuesday", "Wednesday", "Thursday"]


    return render_template("dashboard.html", user = user, test = test)

@app.route('/pantry')
def pantry():
    return redirect("/pantry/view")

@app.route('/recipes')
def recipes():
    return render_template("/recipes.html")

@app.route('/pantry/add')
def pantry_add():
    return render_template("/pantry_add.html")

@app.route("/pantry/add/process", methods = ["POST"])
def add_ingredient():

    user_id = session["user_id"]
    
    total_cost = float(request.form["total_cost"])
    quantity = float(request.form["quantity"])
    cost_per_unit = float(total_cost / quantity) 

    data = {
        "ingredient_name": request.form["ingredient_name"],
        "type": request.form["type"],
        "measure_type": request.form["measure_type"],
        "quantity": quantity,
        "total_cost": float(total_cost),
        "cost_per_unit": cost_per_unit,
        "user_id": user_id
    }

    name = data["ingredient_name"]


    Pantry.add_ingredient(data)
    flash(f"Successfully added {name} to the pantry.")
    return redirect("/pantry/add")

@app.route("/pantry/delete/<int:id>")
def delete_ingredient(id):
    
    data = {
        "id": id
    }

    Pantry.delete_ingredient(data)

    return redirect("/pantry/edit")


@app.route("/pantry/edit/<int:id>", methods = ["POST"])
def edit_ingredient(id):
    user_id = session["user_id"]
    
    total_cost = float(request.form["total_cost"])
    quantity = float(request.form["quantity"])
    cost_per_unit = float(total_cost / quantity) 

    data = {
        "id": id,
        "ingredient_name": request.form["ingredient_name"],
        "type": request.form["type"],
        "measure_type": request.form["measure_type"],
        "quantity": quantity,
        "total_cost": float(total_cost),
        "cost_per_unit": cost_per_unit,
        "user_id": user_id
    }

    name = data["ingredient_name"]

    Pantry.edit_ingredient(data)
    flash(f"Successfully edited {name}.")
    return redirect("/pantry/edit")

@app.route('/pantry/use')
def pantry_use():
    today = date.today()

    today_string = today.strftime("%Y-%m-%d")

    print(today_string)

    data = {"user_id": session["user_id"]}

    all_ingredients = Pantry.get_all_ingredients(data)
    
    return render_template("/pantry_use.html", all_ingredients = all_ingredients, today = today_string)

@app.route('/pantry/edit')
def pantry_edit():    

    data = {"user_id": session["user_id"]}

    all_ingredients = Pantry.get_all_ingredients(data)
    
    return render_template("/pantry_edit.html", all_ingredients = all_ingredients)

@app.route('/pantry/view')
def pantry_view():

    data = {"user_id": session["user_id"]}

    all_ingredients = Pantry.get_all_ingredients(data)
    
    return render_template("/pantry.html", all_ingredients = all_ingredients)


@app.route('/pantry/use/process', methods = ['POST'])
def pantry_use_ingredient():
    quantity_used = float(request.form["quantity_used"])
    data = {
        "id": request.form["ingredient_id"],
    }

    ingredient = Pantry.get_by_id(data)
    current_quantity = float(ingredient.quantity)

    if quantity_used > current_quantity:
        flash(f"You only have {ingredient.quantity} {ingredient.ingredient_name} in stock.")
        return redirect("/pantry/use")

    
    total_cost = quantity_used * float(ingredient.cost_per_unit)
    quantity = current_quantity - quantity_used

    

    data = {
        "pantry_id": request.form["ingredient_id"],
        "user_id": session["user_id"],
        "use_date": request.form["use_date"],
        "quantity_used": request.form["quantity_used"],
        "use_type": request.form["use_type"],
        "total_cost": total_cost,
        "quantity": quantity
    }

    name = ingredient.ingredient_name

    Pantry.use_ingredient(data)

    flash(f"Successfully used {name} from the pantry.")

    return redirect('/pantry/use')

@app.route('/costs')
def costs():
    return render_template("/costs.html")

@app.route('/costs/custom')
def costs_custom():
    return render_template("/costs_custom.html")

@app.route('/costs/daily')
def costs_daily():
    start_date = date.today()

    data = {
        "user_id": session["user_id"],
        "end_date": start_date
    }
    
    daily_transactions = History.get_daily_history(data)

    total = daily_transactions[0]["daily_total"]

    blah = daily_transactions.pop(0)

    return render_template("/costs_daily.html", daily_transactions = daily_transactions[0], total = round(total,2))

@app.route('/costs/weekly')
def costs_weekly():
    end_date = date.today()
    start_date = end_date - timedelta(days = 6)
    
    data = {
        "user_id": session["user_id"],
        "start_date": start_date,
        "end_date": end_date
    }
    
    weekly_transactions = History.get_weekly_history(data)

    total = weekly_transactions[0]["weekly_total"]

    blah = weekly_transactions.pop(0)

    return render_template("/costs_weekly.html", daily_transactions = weekly_transactions[0], total = round(total,2))

@app.route('/costs/history')
def costs_history():
    end_date = date.today()
    week_start_date = end_date - timedelta(days = 6)    

    user = User.get_by_id({"user_id": session["user_id"]})
    
    data = {
        "user_id": session["user_id"],
        "start_date": week_start_date,
        "end_date": end_date
    }
    daily_transactions = History.get_daily_history(data)
    daily_total = daily_transactions[0]["daily_total"]
    blah = daily_transactions.pop(0)

    
    days_of_week = ["a","a","a","a","a","a","a"]
    daily_totals = [1,1,1,1,1,1,1]
    adjustment = [1,1,1,1,1,1,1]
    color = ["a","a","a","a","a","a","a"]
    counter = 0
    for i in range (6, -1, -1):

        day_of_week = end_date + timedelta(days = -i)
        days_of_week[counter] = day_of_week.strftime("%a")
        
        data = {
        "user_id": session["user_id"],
        "end_date": day_of_week
        }
        transaction = History.get_daily_history(data)

        daily_totals[counter] = round(transaction[0]["daily_total"],2)

        adjustment[counter] = daily_totals[counter] * 2
        
        if daily_totals[i] < 20:
            color[counter] = "green"
        elif daily_totals[i] < 30:
            color[counter] = "yellow"
        else:
            color[counter] = "red"  

        counter += 1

    month_start_date = date(int(end_date.year), int(end_date.month), 1)
    data = {
        "user_id": session["user_id"],
        "start_date": month_start_date,
        "end_date": end_date
    }

    monthly_transactions = History.get_weekly_history(data)
    monthly_total = monthly_transactions[0]["weekly_total"]
    blah = monthly_transactions.pop(0)

    return render_template("/costs_history.html", days_of_week = days_of_week, daily_totals = daily_totals, adjustment = adjustment, color = color, user = user, daily_total = daily_total, monthly_total = monthly_total, daily_transactions = daily_transactions[0], monthly_transactions = monthly_transactions[0])

@app.route("/recipes/create")
def create_recipe():
    
    return render_template("/recipes_create.html")

@app.route('/login/process', methods=['POST'])
def login_user():
    
    data = {"username" : request.form["username"]}
    
    user_in_db = User.get_by_username(data)
    
    if not user_in_db:
        flash("Invalid Username or Password")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email or Password")
        return redirect('/login')
    
    session['user_id'] = user_in_db.id
    
    return redirect("/dashboard")

@app.route('/logout')
def logout_sucessful():
    session.clear()
    return redirect("/")
