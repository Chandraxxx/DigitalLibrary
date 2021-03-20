from flask import Flask, render_template, \
  request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = "1q2w3e4r5t"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#membuat objek dari kelas SQLAlchemy
db = SQLAlchemy(app)

#mendefinisikan model
class User(db.Model):
        __tablename__='user'
        id=db.Column("id", db.String(10), primary_key=True)
        name = db.Column(db.String(100))
        level = db.Column(db.String(10))
        password = db.Column(db.String(100))       

        def __init__(self, id, name, level, password):
                self.id=id
                self.name=name
                self.level=level
                self.password=password

        def __repr__(self):
                return '[%s, %s, %s, %s]' % \
         (self.id, self.name, self.level, self.password)
        
class File(db.Model):
        __tablename__="file"
        idF = db.Column("idF", db.String(10), primary_key=True)
        nameF = db.Column("nameF", db.String(100))
        hostF = db.Column("hostF", db.String(100))    
        linkF = db.Column("linkF", db.String(10000))
        datesF = db.Column("datesF", db.DateTime)

        def __init__(self, idF, nameF, hostF, linkF, datesF):
                self.idF = idF
                self.nameF = nameF
                self.hostF = hostF
                self.linkF = linkF
                self.datesF = datesF

@app.route('/',methods=["POST","GET"])
def index():
        exists = User.query.filter_by(name="admin").first()
        if not exists:
       # #firsttime launch isi db dengan satu akun admin.
       #  exists = bool(User.query.filter_by(name='admin').first())
       #  if exists is False:
                user = User("1","admin","Admin","admin")
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("index"))
       #  #kalau sudah ada
        else:
                if "user" in session:
                        return redirect(url_for("panel_Admin"))
                else:
                        if request.method == "POST":
                                uid = request.form['uid']
                                pw = request.form['pw']

                                isUserExist=bool(User.query.filter_by(name=uid).first())
                                if isUserExist == False:
                                        msg2 = True
                                        return render_template("a_index.html", msg2 = msg2)
                                else:
                                        user = User.query.filter_by(name=uid).first()
                                        if user.password == pw:
                                                session['user'] = uid
                                                return redirect(url_for("panel_Admin"))
                                        else:
                                                msg=True
                                                return render_template("a_index.html", msg=msg)
                        else:
                                return render_template("a_index.html")

@app.route('/aboutMe')
def aboutMe():
        return render_template("aboutme.html")

@app.route('/addUser', methods = ["POST", "GET"])
def add_Users():
        if request.method=="POST":
                id = request.form['id']
                username = request.form['username']
                level = request.form['level']
                password = request.form['password']
                user = User(id,username, level, password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("users"))
        else:
                return render_template("reg_users.html")
        return render_template("reg_users.html")

@app.route('/del_User/<id>', methods = ["POST","GET"])
def del_User(id):
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users'))

@app.route('/edit_User/<id>', methods=["POST","GET"])
def edit_User(id):
        user = User.query.filter_by(id=id).first()
        if request.method == 'POST':
                user = User.query.get(request.form['id'])                
                user.name = request.form['username']
                user.level = request.form['level']
                user.password = request.form['password']                
                db.session.commit()
                return redirect(url_for("users"))       
        else:
                return render_template("edit_user.html", container=user)


@app.route ('/delUser/<id>', methods = ["POST", "GET"])
def delUsers(id):
        
        return redirect(url_for("users"))

# @app.route('/admin', methods = ["POST", "GET"])
# def admin_page():
#         #firsttime launch isi db dengan satu akun admin.
#         exists = bool(User.query.filter_by(name='admin').first())
#         if exists is False:
#                 user = User("1","admin","Admin","admin")
#                 db.session.add(user)
#                 db.session.commit()
#         #kalau sudah ada
#         else:
#                 if "user" in session:
#                         return redirect(url_for("panel_Admin"))
#                 else:
#                         if request.method == "POST":
#                                 uid = request.form['uid']
#                                 pw = request.form['pw']

#                                 isUserExist=bool(User.query.filter_by(name=uid).first())
#                                 if isUserExist == False:
#                                         msg2 = True
#                                         return render_template("a_index.html", msg2 = msg2)
#                                 else:
#                                         user = User.query.filter_by(name=uid).first()
#                                         if user.password == pw:
#                                                 session['user'] = uid
#                                                 return redirect(url_for("panel_Admin"))
#                                         else:
#                                                 msg=True
#                                                 return render_template("a_index.html", msg=msg)
#                         else:
#                                 return render_template("a_index.html")

@app.route('/panel_Admin', methods=["POST","GET"])
def panel_Admin():
        #udah login
                if "user" in session:

                        #adding Files
                        if request.method == "POST":
                                idF=request.form['idF']
                                nameF=request.form['namaF']
                                hostF=request.form['hostF']
                                linkF=request.form['linkF']
                                datesF=datetime.now()
                                file=File(idF, nameF, hostF, linkF, datesF)
                                db.session.add(file)
                                db.session.commit()

                        return render_template("a_panel.html", container=File.query.all())
                #belum login
                else:
                        return redirect(url_for("index"))

@app.route('/del_File/<id>', methods=["POST", "GET"])
def del_File(id):
        file = File.query.filter_by(idF=id).first()
        db.session.delete(file)
        db.session.commit()
        return redirect(url_for("panel_Admin"))

@app.route('/users')
def users():
        if "user" in session:
                return render_template("a_users.html", container=User.query.all())
        else:
                return redirect(url_for("index"))

@app.route('/logout')
def logOut():
        session.pop('user',None)
        return redirect(url_for("index"))

if __name__ == "__main__":
        db.create_all()
        app.run(debug=True)
