from flask_app import app, render_template, request, redirect, session, flash
from flask_app.models.model_recipe import Recipe
from flask_app.models.model_user import User

@app.route("/new")
def new_recipe():
    return render_template("new.html")

@app.route('/process_recipe', methods=['POST'])
def create_recipe():
    
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "date_made" : request.form['date_made'],
        "under_30" : request.form['under_30'],
        "user_id" : session['id']
    }

    if not Recipe.validate_recipe(request.form):
        return redirect('/')
        
    Recipe.save(data)
    id = session['id']
    return redirect(f"/dashboard/{id}")
    

@app.route("/recipes/<int:id>")
def show_recipe(id):
    print("Showing the User Info From the Form")
    data = {
        "id":id
        }
    data2 = {
        "id": session['id']
    }
    recipe=Recipe.get_one(data)
    user=User.get_one(data2)
    return render_template("recipes.html", recipe=recipe, user=user )

@app.route("/edit/<int:id>")
def edit(id):
    data = {"id":id}
    return render_template("edit.html", recipe= Recipe.get_one(data))

@app.route('/update',methods=['POST'])
def update():
    Recipe.update(request.form)
    id = session['id']
    return redirect(f"/dashboard/{id}")

@app.route("/destroy/<int:id>")
def destroy(id):
    data ={'id': id}
    Recipe.destroy(data)
    id = session['id']
    return redirect(f"/dashboard/{id}")

