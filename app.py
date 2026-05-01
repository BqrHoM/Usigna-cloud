import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, jsonify , url_for , send_from_directory
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import re
import subprocess
import requests
from adds import oops , pw_check , size_of_user ,  login_required , premium ,storage_type_premium , storage_type_free , change



app = Flask (__name__)



app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#making new route containing the image
@app.route("/drive/<int:user_id>/<path:filename>")
def render_image (user_id, filename):
    return send_from_directory(f"drive/{user_id}", filename)


@app.route ("/register" , methods =["GET","POST"])
def register ():

    #Checking if the user is logged in
    if session.get("_user_id"):
        return redirect ("/")

    if request.method == "POST":

        #Importing the variable from the form
        email = request.form.get ("email")
        password = request.form.get ("password")
        confirm_password = request.form.get("confirm_password")

        #checking if the email or the passwords slots are empty
        if not email  :
            return oops ("You should enter a valid Email" ,400)
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email) != None :
            return oops ("Your Email format is not correct" ,400)

        if not password :
            return oops ("You should enter a valid password" ,400)
        if not confirm_password :
            return oops ("You should confirm your password" ,400)

        #checking if the passwords match
        if password != confirm_password :
            return oops ("Passwords do not match" ,400)
        if not pw_check(password):
            return oops ("Your password should at least contain 8 characters , with at least one Capital and Lower letter , one number , and one special character" ,400)
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        #Checking if the email is already used
        cur.execute("SELECT * FROM users WHERE mail = ?" , (email,))
        data = cur.fetchone()

        if data != None :
            conn.close()
            return oops("This email is already used !" ,400)

        #Inserting the user data into the data base
        hash = generate_password_hash(password)
        storage_type_free = 0
        storage_type_premium = 0
        cur.execute ("INSERT INTO users (mail , hash ,premium ,storage_type_premium ,storage_type_free ) VALUES (? , ? , ? , ? , ? )" , (email , hash ,False , storage_type_premium  ,storage_type_free , ))
        conn.commit()

        cur.execute("SELECT * FROM users WHERE mail = ?" , (email,))
        data = cur.fetchone()
        session["_user_id"] =data[0]

        conn.close()
        return redirect ("/")
    return render_template("register.html")


@app.route("/" , methods =["GET"])
def index():
    return render_template("index.html")




@app.route ("/login", methods = ["GET" , "POST"])
def login ():

    if session.get("_user_id"):
        return redirect ("/")



    if request.method == "POST" :

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        # getting the input of the user
        email = request.form.get("email")
        password = request.form.get("password")

        #checking if the email or the password slots are empty
        if not email :
            return oops ("You should enter a valid Email" ,400)
        if not password :
            return oops ("You should enter a valid password" ,400)


        # Importing the user data from the database
        cur.execute ("SELECT * FROM users WHERE mail =?" , (email ,))
        data = cur.fetchone()

        #checking if the email is invalid
        if data == None :
            conn.close()
            return oops("WRONG EMAIL !" , 400)



        #taking the hash from the data base
        data_hash = data[2]



        #checking if the password is incorrect
        if not check_password_hash(data_hash ,password) :
            conn.close()
            return oops ("PASSWORD DOESN'T MATCH ")

        # Giving the user the session as he logged in
        session["_user_id"] =data[0]
        conn.close()
        return redirect ("/")

    # direct the user to the login page
    return render_template ("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/about")
def about():
    return render_template ("about.html")

@app.route("/addservice" , methods = ["GET","POST"])
@login_required
def add_service ():


    #TAKING the all of the user's data
    premium_check = premium()
    size = size_of_user (session["_user_id"])
    ps = storage_type_premium()
    fs = storage_type_free()
    drive = request.form.get("drive")
    limit = 0
    if fs :
        limit = limit + 51200
    if ps :
        limit = limit + 102400

    if request.method == "POST":
        if not ps and not fs :
            id = session["_user_id"]
            folder = "drive/" + str(id)
            os.makedirs(folder , exist_ok=True)
        if drive == "free" and fs  :
            return oops("You have already Taken this !",401)
        elif drive == "premium" and ps:
            return oops("You have already Taken this !",401)
        if drive == "free":
            change ("free")
            return render_template ("pursh.html" , a= "You have successfully Taken the free offer!")
        elif drive == "premium":
            change ("premium")
            return render_template ("pursh.html" , a= "You have successfully Taken the premium offer!")
    if limit-size <= 0:
        avaiblee = "OUT OF STORAGE"
    else :
        avaiblee = limit-size


    return render_template ("add.html", premium_check = premium_check , size = size , ps =ps , fs =fs , avaible= avaiblee)


@app.route("/activate" , methods = ["GET","POST"])
@login_required
def activate():
    test = premium()
    if request.method == "POST":
        code = request.form.get("code")
        if str(code) =="123" :
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            s=session.get("_user_id")
            cur.execute("UPDATE users SET premium = 1 WHERE id = ? " , (s ,))
            conn.commit()
            conn.close()
            return render_template ("pursh.html" , a= "You have successfully Activated Your Account !")
        else :
            return oops("Your code is unavailable !" , 401)
    return render_template ("activate.html" , test=test)


@app.route("/manage" , methods = ["GET","POST"])
@login_required
def manage():


    id=session.get("_user_id")

    if request.method == "POST":
        image = request.files["image"]
        limit=0
        image_size = len(image.read()) // 1024
        image.seek(0)
        size = size_of_user (session["_user_id"])
        ps = storage_type_premium()
        fs = storage_type_free()
        if fs :
            limit = limit + 51200
        if ps :
            limit = limit + 102400


        os.makedirs(f"drive/{id}", exist_ok=True)
        if limit == 0 :
            return oops ("You have not added a service !",400)
        elif size < limit :
            image.save(f"drive/{id}/{ secure_filename(image.filename)}")
        else :
            return oops("You have already passed your storage limit",400)


        return redirect ("/manage")
    os.makedirs(f"drive/{id}", exist_ok=True)
    files = os.listdir(f"drive/{id}/")
    files = [url_for('render_image', user_id=id, filename=f) for f in files]

    return render_template ("manage.html" , files=files)


@app.route("/backup", methods=["GET", "POST"])
@login_required
def backup():
    import requests, os

    if request.method == "POST":
        #getting the user id and the path of his drive and making it in case it doesn't exist
        id = session.get("_user_id")
        folder_path = f"drive/{id}"
        os.makedirs(folder_path, exist_ok=True)

        SERVER = "https://mellissa-syndesmotic-twangily.ngrok-free.dev"

        #Getting the user files from his drive
        files = os.listdir(folder_path)

        if not files:
            return oops("No files found to back up!", 400)
        num_uploaded = 0
        num_failed = 0

        for filename in files:
            file_path = os.path.join(folder_path, filename)
            try:

                with open(file_path, "rb") as file_data:

                    response = requests.post(f"{SERVER}/drive" , files = {"file": (filename, file_data)}, data={ "user_id" :id} ,timeout = 10 )


                if response.status_code == 200:
                    num_uploaded += 1
                else:
                    num_failed += 1
            except requests.exceptions.RequestException as e:
                num_failed += 1


        message = f"✅ Uploaded: {num_uploaded} | ❌ Failed: {num_failed}"

        return render_template("backup_check.html", ch=message)

    return render_template("backup.html")
