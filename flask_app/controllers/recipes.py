from flask import Flask, redirect, render_template, request, session, flash
from flask_app import app
from flask_app.models.recipe import Recipes
from flask_app.models.user import Users

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id': session['user_id']
    }
    return render_template('new_recipe.html', id=Users.get_id(data), recipes=Recipes.get_all())

# Create Recipe Page
@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    
    
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],

        "user_id": session["user_id"],
    }
    Recipes.save(data)
    return redirect("/dashboard")

#View all under one user
@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data =  {
        "id": id,
    }
    user_data = {
        "user_id": session["user_id"],
    }
    return render_template("dashboard.html", one_recipe=Recipes.get_one(data), user=Users.get_id(user_data))

#grab and show one from all_recipes
@app.route("/recipes/<int:id>")
def show_one(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data =  {
        "id": id,
    }
    user_data = {
        "id": session["user_id"],
    }
    return render_template(
        "show.html", 
        one_recipe=Recipes.get_one(data), 
        user=Users.get_id(user_data))


#update
@app.route("/update/recipes", methods=["POST"])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    
    
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "id": request.form["recipe_id"],
    }
    Recipes.update(data)
    return redirect("/dashboard")


@app.route("/update/recipes/<int:id>")
def edit_one(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data =  {
        "id": id,
    }
    user_data = {
        "id": session["user_id"],
    }
    return render_template(
        "edit_recipe.html", 
        one_recipe=Recipes.get_one(data), 
        user=Users.get_id(user_data))




#delete 
@app.route("/delete/recipes/<int:id>")
def delete(id):
    data =  {
        "id": id,
    }
    Recipes.delete(data)
    return redirect("/dashboard")
