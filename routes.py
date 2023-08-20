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
    conn = sqlite3.connect("wallpapers.db")
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM photos").fetchall()
    rating = cur.execute("SELECT rating FROM photos").fetchall()
    cookieURL = request.cookies.get('URL')
    return render_template("layout.html", data=data, rating=rating, cookieURL=cookieURL,)                                                                                               


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    conn = sqlite3.connect("wallpapers.db")
    cur = conn.cursor()
    tag = request.form['name_v']
    data = cur.execute("INSERT INTO photos ('tag') VALUES (?)", (tag,))
    cur.connection.commit()                                                                                                                                                               
    return render_template("layout.html")

@app.route("/contact")
def contact(): 
    return render_template("contact.html")


app.config["Image_path1"] = "C:/Users/cheni/Documents/dtpproject-/dtpproject/static/images"
app.config["Image_path2"] = "H:\dtpproject-master\dtpproject-master\static\images"

@app.route("/fileupload", methods=['GET', 'POST'])
def fileupload(): 
    isvalid = "Nothing"
    if request.method == 'POST': 
        conn = sqlite3.connect("wallpapers.db")
        cur = conn.cursor()
        tag = request.form['tag']
        file = request.files['filename']
        extension = file.filename.split('.')

        if extension[1] == "jpg" or extension[1] == "png" or extension[1] == "jpeg" :
            file.save(os.path.join(app.config["Image_path1"], (tag  + "." + extension[1])))
            data = cur.execute("INSERT INTO photos ('image', 'rating') VALUES (?, ?)", (tag + "." + extension[1], 0))
            cur.connection.commit()  
            app.logger.debug("true")
            isvalid = "OK"
        else: 
            app.logger.debug("error")
            isvalid = "Error"
       
            
    return render_template("fileupload.html", isvalid=isvalid,)



@app.route("/viewfiles/<imageurl>")
def viewfiles(imageurl): 
    conn = sqlite3.connect("wallpapers.db")
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM photos").fetchall()
    rating = cur.execute("SELECT rating FROM photos").fetchall()
    cookieURL = request.cookies.get('URL')
    
    return render_template("readfile.html", data=data, rating=rating, imageurl=imageurl,)

@app.route("/delete/<filename>")  #admin only 
def delete(filename):
    conn = sqlite3.connect("wallpapers.db")
    cur = conn.cursor()
    data = cur.execute("DELETE FROM photos WHERE image=?", (filename,)) #delete all files where image name matches
    os.remove(os.path.join(app.config['Image_path1'], filename))
    cur.connection.commit()
    return redirect("/viewfiles/0")


@app.route('/download/<filename>') 
def download(filename): 
    print(filename)
    return send_file(os.path.join(app.config["Image_path1"], filename), filename, as_attachment=True) 

#join all the variables as a path to download the file


@app.route('/submitreview/<imageurl>/<rating>')
def review(imageurl, rating):
    cookieURL = request.cookies.get(imageurl)   
    if cookieURL == imageurl:
        return redirect(url_for("viewfiles", imageurl=imageurl,))
    else:
        conn = sqlite3.connect("wallpapers.db")
        cur = conn.cursor()
        data = cur.execute("UPDATE photos SET rating=rating + (?) WHERE image=(?)", (int(rating), imageurl)) #upadate rating in database
        cur.connection.commit()
        resp = make_response(redirect(url_for('viewfiles', imageurl="none", ))) #make a new cookie, and store the imageurl in it
        resp.set_cookie(imageurl, imageurl)
        print(resp)
        return resp



@app.route('/lucky')
def lucky():
    conn = sqlite3.connect("wallpapers.db")
    cur = conn.cursor()
    data = cur.execute("SELECT COUNT(*) as totalphotos FROM photos").fetchone()
    numPhotos = data[0]
    app.logger.debug(random.randint(0, numPhotos))
    return render_template ("fileupload.html")

if __name__ == "__main__": 
    app.run(debug=True)


