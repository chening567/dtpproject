from flask import Flask, render_template, redirect, url_for, request, send_file, make_response
from io import BytesIO
from werkzeug.utils import secure_filename
import os
import sqlite3
import random
import datetime

app = Flask(__name__)


@app.route("/") 
def home():
    data = database_connection("SELECT * FROM photos", None, False)
    rating = database_connection("SELECT * FROM photos", None, False)   
    return render_template("readfile.html", data=data, rating=rating,
                           )   

def database_connection(statement, data, insert): #if insert == true, then insert statement + data into sql database, else return data from statement
    conn = sqlite3.connect("wallpapers.db")
    cur = conn.cursor()
    if insert == True: 
        exe = cur.execute(statement, data)
        cur.connection.commit()
        return None
    else: 
        exe = cur.execute(statement).fetchall()
        cur.connection.commit()
        return exe

@app.route("/upload", methods=['GET', 'POST'])#set methods to GET and POST
def upload():
                                                                                                                                                                
    return render_template("layout.html")


@app.route("/contact")
def contact(): 
    return render_template("contact.html")


app.config["Image_path1"] = "C:/Users/cheni/Documents/dtpproject-/dtpproject/static/images" #image oath for server at home
app.config["Image_path2"] = "H:\dtpproject-master\dtpproject-master\static\images" 

#file upload route
@app.route("/fileupload", methods=['GET', 'POST'])
def fileupload(): 
    isvalid = "Nothing"
    if request.method == 'POST': 
        tag = request.form['tag']
        file = request.files['filename']
        extension = file.filename.split('.')
        if extension[1] == "jpg" or extension[1] == "png" or extension[1] == "jpeg" and len(file) > 0: #if file is suported then insert data into server and file name into database
            file.save(os.path.join(app.config["Image_path1"], (tag  + "." + extension[1])))
            database_connection("INSERT INTO photos ('image', 'rating') VALUES (?, ?)", (tag + "." + extension[1], 0), True)
            app.logger.debug("true")
            isvalid = "OK" #set valid to OK and send variable into html
        else: 
            app.logger.debug("error")
            isvalid = "Error"  
    return render_template("fileupload.html", isvalid=isvalid,)
 
#view files route
@app.route("/viewfiles/<imageurl>")
def viewfiles(imageurl): 
    data = database_connection("SELECT * FROM photos", None, False)
    rating = database_connection("SELECT * FROM photos", None, False)   
   
    
    return render_template("readfile.html", data=data, rating=rating,
                           imageurl=imageurl,)


# admin only 



@app.route('/download/<filename>')
def download(filename):
    print(filename)

    return send_file(os.path.join(app.config["Image_path1"], filename), filename, as_attachment=True) 
    # join all the variables as a path to download the file



@app.route('/submitreview/<imageurl>/<rating>')
def review(imageurl, rating):
    cookieURL = request.cookies.get(imageurl)   
    if cookieURL == imageurl: #checking if the user has already rated the image
        return redirect(url_for("viewfiles", imageurl=imageurl,))
    else:
        database_connection("UPDATE photos SET rating=rating + (?) WHERE image=(?)", (int(rating), imageurl), True)
        # make a new cookie, and store the imageurl in it
        
        imageCookie = make_response(redirect(url_for('viewfiles', imageurl="none", ))) 
        imageCookie.set_cookie(imageurl, imageurl)
        
        return imageCookie


@app.route("/lucky/<url>")
def lucky(url):
    conn = sqlite3.connect("wallpapers.db")
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM photos").fetchall()
    rating = cur.execute("SELECT rating FROM photos").fetchall()
    randomVal = random.randint(0, len(data)) 
    app.logger.debug(data[randomVal-1][1])
    
    return render_template("lucky.html", data=data, rating=rating,
                           url=url, randomVal=randomVal)

#admin stuff

password = "qpwoeirituy"
typed = False #stop people from typing in link and accessing admin
@app.route("/admin/login", methods=['GET', 'POST'])
def adminLogin(): 
    global password
    global typed
    if request.method == 'POST': 
        formRequest = request.form['password']
        if formRequest == password:
            typed = True
            return redirect("/admin/0")
        else:
            return redirect("/admin/login")
    return render_template("login.html")
        
@app.route("/admin/<imageurl>")
def adminfiles(imageurl): 
    global typed
    if typed == True: #stop people from typing in link and accessing admin
        conn = sqlite3.connect("wallpapers.db")
        cur = conn.cursor()
        data = cur.execute("SELECT * FROM photos").fetchall()
        rating = cur.execute("SELECT rating FROM photos").fetchall()
        cookieURL = request.cookies.get('URL') 
        return render_template("admin.html", data=data, rating=rating, imageurl=imageurl,)
    else: 
        redirect("/admin/login")

@app.route("/delete/<filename>")
def delete(filename):
    conn = sqlite3.connect("wallpapers.db")
    cur = conn.cursor()
    # delete all files where image name matches
    data = cur.execute("DELETE FROM photos WHERE image=?", (filename,))

    os.remove(os.path.join(app.config['Image_path1'], filename))
    cur.connection.commit()
    return redirect("/admin/0")


if __name__ == "__main__":
    app.run(debug=True)



