from flask import Flask, flash, redirect, render_template, request, session, jsonify
from functools import wraps
import sqlite3
import subprocess


def oops (ch ,n):
    return render_template ("problem.html" , ch = ch , n=str(n))

def size_of_user (user):
    #taking the folder path
    folder = "drive/" + str(user) + "/"
    try:
        #checking the space occupied by the user folder
        s = int(subprocess.check_output(['du' , '-s' , folder]).decode().split()[0])

    except subprocess.CalledProcessError :
        return 0
    return s

def pw_check(ch):
    test1= False
    test2=False
    test3=False
    test4=False
    for letter in ch :

        if letter.isupper() and not test1:
            test1 = True
        if letter.islower() and not test2:
            test2 = True
        if not letter.isalnum() and not test3:
            test3 = True
        if len(ch)>8 and not test4:
            test4 = True
        if test1 and test2 and test3 and test4 :
            break

    return (test1 and test2 and test3 and test4)


def login_required(f):
    # I used chat gpt to know how to use the decorator
    @wraps(f)
    def wrapper(*args, **kwargs):

        if session.get("_user_id") :
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            cur.execute ("SELECT * FROM users WHERE id =?" , (session["_user_id"] ,) )
            data = cur.fetchone()

            #checking if the email is invalid
            if data == None :
                conn.close()
                session.clear()
                return oops("Your session is invalid !",401)
            return f(*args, **kwargs)

        else :
            return oops("Please log in to access this content",401)
    return wrapper


def premium():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    a=session["_user_id"]
    cur.execute("SELECT premium FROM users WHERE id = ?", (a,))

    data = cur.fetchone()[0]
    if int (data)==0:
        conn.close()
        return False
    conn.close()
    return True


def storage_type_premium  ():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    a=session["_user_id"]
    cur.execute("SELECT storage_type_premium  FROM users WHERE id = ?", (a,))
    data = cur.fetchone()[0]
    conn.close()
    return bool(int(data))




def storage_type_free  ():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    a=session["_user_id"]
    cur.execute("SELECT storage_type_free  FROM users WHERE id = ?", (a,))
    data = cur.fetchone()[0]
    conn.close()
    return bool(int(data))



def change  (f):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    a=session["_user_id"]
    ch=f" UPDATE users SET storage_type_{f} = 1 WHERE id = ? "
    cur.execute(ch , ( a,))
    conn.commit()

    conn.close()
    return

