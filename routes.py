from flask import Flask, render_template, redirect, url_for, request, send_file

from io import BytesIO
from werkzeug.utils import secure_filename
import os
import sqlite3
import random



app = Flask(__name__)
@app.route("/") 
def home():                                                                                               
    return render_template("layout.html")


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
        if extension[1] == "jpg" or extension[1] == "png" or extension[1] == "gif" :
            
            file.save(os.path.join(app.config["Image_path1"], (tag  + "." + extension[1])))
            data = cur.execute("INSERT INTO photos ('image') VALUES (?)", (tag + "." + extension[1],))
            cur.connection.commit()  
            app.logger.debug("true")
            isvalid = "OK"
        else: 
            app.logger.debug("error")
            isvalid = "Error"
       
            
    return render_template("fileupload.html", isvalid=isvalid,)

@app.route("/viewfiles")
def viewfiles(): 
    conn = sqlite3.connect("wallpapers.db")
    cur = conn.cursor()
    data = cur.execute("SELECT image FROM photos").fetchall()

    

    return render_template("fileupload.html", data=data,)

@app.route('/viewfiles/<filename>')
def download(filename): 
    print(filename)
    return send_file(os.path.join(app.config["Image_path1"], filename), filename, as_attachment=True)

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


