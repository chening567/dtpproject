from flask import Flask, render_template, redirect, url_for, request, send_file

from io import BytesIO
import sqlite3



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
    print(tag)                                                                                                                                                            
    return render_template("layout.html")

@app.route("/contact")
def contact(): 
    return render_template("contact.html")




@app.route("/fileupload", methods=['GET', 'POST'])
def fileupload(): 
    if request.method == 'POST': 
        conn = sqlite3.connect("wallpapers.db")
        cur = conn.cursor()
        tag = request.form['tag']
        file = request.files['filename']
        bfile = file.read()
        
        data = cur.execute("INSERT INTO photos ('tag', 'image') VALUES (?, ?)", (tag, bfile,))
        cur.connection.commit()   
    return render_template("fileupload.html")

#* @app.route("/readfile")
#def readfile():
    #conn = sqlite3.connect("wallpapers.db")
   # cur = conn.cursor()
  #  rec = cur.execute("SELECT image FROM photos").fetchall()
    
 #   print(rec[2])
#    return send_file(BytesIO(rec[2]), attachment_filename="brrr", as_attachment=True)

@app.route('/download/<upload_id>')
def download(upload_id):
    conn = sqlite3.connect("wallpapers.db")
    cur = conn.cursor()
    rec = cur.execute("SELECT image FROM photos").fetchall()
    upload = (rec[1])
    print(upload)
    return send_file(BytesIO(upload),
                     download_name="dwijdiw", as_attachment=True)


if __name__ == "__main__": 
    app.run(debug=True)


