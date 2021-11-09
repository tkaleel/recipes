from flask_app import app, render_template, request, redirect, session, flash
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')         
def index():
    return render_template("index.html")

@app.route('/process_user', methods=['POST'])
def create_user():

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email_address" : request.form['email_address'],
        "password" : pw_hash,
        "confirm_password" : request.form['confirm_password']
    }

    if not User.validate_user(request.form):
        return redirect('/')
        
    id= User.save(data)
    session['id'] = id
    return redirect(f"/dashboard/{id}")
    

@app.route("/dashboard/<int:id>")
def show_user(id):
    print("Showing the User Info From the Form")
    if 'id' not in session:
        return redirect('/logout')
    data = {
        "id":id
        }
    user=User.get_one(data)
    return render_template("dashboard.html", user=user, user_recipes= User.get_user_with_recipes(data) )


@app.route("/login", methods=['POST'])
def login():
    data = {
        "email_address" : request.form["email_address"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['id'] = user_in_db.id
    id = user_in_db.id
    return redirect(f"/dashboard/{id}")

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
