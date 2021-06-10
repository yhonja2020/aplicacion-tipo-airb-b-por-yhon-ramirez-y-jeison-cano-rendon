import pymongo 
import json

from pymongo.results import UpdateResult
myClient = pymongo.MongoClient("mongodb://localhost:27017")# conexion 
myDb= myClient["proyectapp"] # database
usersCol = myDb["users"]
usersAdd = myDb["addliving"]


# myLogin = {"name": "Yhon Ramirez", "password": "Junior6789"}

# result= myCollection.insert_one(myLogin)
# print(result)

from flask import Flask, render_template, request, jsonify, redirect, url_for, \
    flash, session, abort

from flask_login import LoginManager, UserMixin, current_user, \
                                login_required, login_user, logout_user 

from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'dartagan'
login_manager = LoginManager(app)
login_manager.login_view = '/login'

@app.route('/',methods = ['GET'])
def home():
    home = usersAdd.find()
    response = []
    for anfitrion in home:
        response.append(anfitrion)
    return render_template('invitado.html', elements=response)

@app.route('/login',methods = ['GET', 'POST']) # decorador permite que el usuario naveguen por diferentes seccion de nuestra web
def proyecto():
    print("A")
    try:
        if request.method == "GET":
            if current_user.is_authenticated:
                idUser = usersCol.find_one({"_id": current_user.idUser})
                if idUser["rol"] == "Anfitrion":
                    return redirect(url_for('admin_filter', id=current_user.idUser))
                else:
                    return redirect(url_for('home'))
            else:
                return render_template("login.html")
        elif request.method == "POST" and request.form is not None:
            if current_user.is_authenticated:
                return redirect(url_for('admin_filter', id=current_user.idUser))
            idUser = usersCol.find_one({"_id": request.form["email"]})
            if idUser and User.check_password(idUser['password'], request.form["password"]):
                print("C")
                user_obj = User(idUser=idUser['_id'], rol=idUser["rol"])
                login_user(user_obj)
                if idUser["rol"] == "Anfitrion":
                    return redirect(url_for('admin_filter', id=current_user.idUser))
                else:
                    return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta.")
                return redirect("/login")
    except Exception as e:
        print("Error {1}", e)
    # if request.method == 'POST':
    #    if idUser is None:
    #         flash("Usuario no existe")
    #         return redirect("/login")
    #     if idUser and User.check_password(request.form["password"], idUser['password']) :
    #         #return jsonify(idUser)
    #         login_user(user, remember=remember)
    #         return redirect("/")
    #     else:
    #         flash("Contraseña inconrrecta.")
    #         return redirect("/login")
    # else:
    #     return render_template("login.html")

    
@app.route('/record/',methods = ['GET', 'POST'])
def record():
    if request.method == "GET":
         return render_template("record.html")
    elif request.method == "POST" and request.form is not None:
        id = request.form['email']
        nombre = request.form['nombre']
        email = request.form['email']
        pais = request.form['pais']
        ciudad = request.form['ciudad']
        password = request.form['password']
        rol = request.form['rol']
        
        query = usersCol.find_one({"email": request.form['email']})
        if query: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect('/record')

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        query = {"_id": id, "nombre":nombre ,"email": email,"pais":pais,"ciudad":ciudad ,"password": password,"rol":rol}
       
        data = usersCol.insert_one(query)
        flash("guardado exitoso.")
        return redirect('/record')



@app.route('/users',methods = ['GET'])
def users():
    users = usersCol.find()
    response = []
    for user in users:
        response.append(user)
    return render_template('users.html', elements=response)
    #return jsonify(response)


    # @app.route('/index/') 
    # def index():
    #     return render_template("index.html")

@app.route('/registerAP/',methods = ['GET', 'POST'])
@login_required
def registerAP():
    idUser = usersCol.find_one({"_id": current_user.idUser})
    if request.method == "GET" and idUser["rol"] == "Anfitrion" :
         return render_template("registerAP.html")
    elif request.method == "POST" and request.form is not None and idUser["rol"] == "Anfitrion" :
        #_id = request.form['id']
        ciudad = request.form['ciudad']
        pais = request.form['pais']
        address = request.form['address']
        ubicacion = request.form['ubicacion']
        rooms = request.form['rooms']
        imgAp = request.form['imgAp']
        imgppal = request.form['imgppal']
        price = request.form['price']
        reseña = request.form['reseña']
        userid = idUser['_id']
        
        query = {"ciudad":ciudad ,"pais": pais,"address":address,"ubicacion":ubicacion ,"rooms": rooms,"imgAp":imgAp,"imgppal": imgppal,"price": price,"reseña": reseña, "reservada": "false", "hostid": "", "userid": userid}
        data = usersAdd.insert_one(query)
        # return jsonify("success inserted:  {}".format(data.inserted_id))
        flash("guardado exitoso.")
        return redirect(url_for("home"))
    else:
        flash("Debe ser anfitrion.")
        return redirect(url_for("home"))

@app.route('/updateAP/<id>',methods = ['GET','POST'])
@login_required
def updateAP(id):
    print(id)
    idAdd = usersAdd.find({"_id": ObjectId(id)})
    if  request.method == "GET":
        apartamentos = []
        for app in idAdd:
            print(app)
            apartamentos.append(app)
        return render_template('updateAP.html', elements=apartamentos)
    elif request.method == "POST":
        ciudad = request.form['ciudad']
        pais = request.form['pais']
        address = request.form['address']
        ubicacion = request.form['ubicacion']
        rooms = request.form['rooms']
        imgAp = request.form['imgAp']
        imgppal = request.form['imgppal']
        price = request.form['price']
        reseña = request.form['reseña']
        reservada = request.form['reservado']
        hostid = request.form['hostid']
        
        
        query = {"ciudad":ciudad ,"pais": pais,"address":address,"ubicacion":ubicacion ,"rooms": rooms,"imgAp":imgAp,"imgppal": imgppal,"price": price,"reseña": reseña, "reservada": "false", "hostid": "", "reservada": reservada, "hostid": hostid}
        newvalues = { "$set": query }
        update = usersAdd.update_one({ "_id": ObjectId(id) }, newvalues, upsert=False)
        
        # return jsonify("success inserted:  {}".format(data.inserted_id))
        
        
        flash("guardado exitoso.")
        return redirect(url_for('admin_filter'))

    


@app.route('/admin/',methods = ['GET'])
def admin_filter():
    idUser = usersCol.find_one({"_id": current_user.idUser})
    if idUser["rol"] == "Anfitrion":
        admin = usersAdd.find({"userid": current_user.idUser })
        response = []
        for anfitrion in admin:
            response.append(anfitrion)
        return render_template('prueba2.html', elements=response)
    else:
        flash("Debe ser anfitrion.")
        return redirect(url_for('home'))

# @app.route('/admin',methods = ['GET'])
# def admin():
#     admin = usersAdd.find()
#     response = []
#     for anfitrion in admin:
#         response.append(anfitrion)
#     return render_template('invitado.html', elements=response)

@app.route('/reservar/<id>',methods = ['GET'])
@login_required
def reservar(id):
    flash("Habitacion Reservada")
    habitacion = usersAdd.find({"_id": ObjectId(id)})
    if habitacion is None:
        return render_template("login.html")
    else:
        idUser = usersCol.find_one({"_id": current_user.idUser})
        if idUser is not None:
            newvalues = { "$set": { "hostid": idUser["_id"], "reservada": "true" } }
            update = usersAdd.update_one({ "_id": ObjectId(id) }, newvalues, upsert=False)
        return redirect(url_for("home"))
    

@app.route('/deleteData/<id>',methods = ['GET'])
def deleteData(id):#eliminar
    query = {"_id": ObjectId(id)}
    print(query, id)
    usersAdd.delete_one(query)
    return redirect(url_for('admin_filter'))


@app.route('/prueba',methods = ['GET'])
def prueba():
    prueba = usersAdd.find()
    response = []
    for anfitrion in prueba:
        response.append(anfitrion)
    return render_template('prueba.html', elements=response)

@app.route('/prueba2',methods = ['GET'])
def login2():
   
    return render_template('prueba2.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


class User:
    def __init__(self, idUser, rol):
        self.idUser = idUser
        self.rol = rol

 
    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.idUser

    @staticmethod
    def check_password(password_hash, password):
        if password_hash == password:
            return True
        else:
            return False

    @login_manager.user_loader
    def load_user(idUser):
        user = usersCol.find_one({"_id": idUser})
        if not user:
            return None
        return User(idUser=user['_id'], rol=user['rol'])


if __name__ == '__main__':
    app.run(host="localhost", port=5002, debug=True)
    #app.run(debug=True)# para no tener que parar el servidor para actualizar web