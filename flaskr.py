from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

#Conexão com o banco
client      = MongoClient('localhost', 27017)
conn        = client['app_gorila']
collection  = conn.profissional


#mentor = collection.profissional

############################
#rota padrão é a rota de login
@app.route('/', methods = ['GET'])
def index():
    return render_template('main/login.html')

#redirecionar para cadastro de profissional

@app.route('/profissionais/new', methods = ['GET', 'POST'])
def new():
     return render_template('/main/profissional/new.html')

#cadastra novo profissional
@app.route('/profissionais/create',  methods=['GET', 'POST'])
def create():
    collection.insert_one({
        'nome': request.form['nome'],
        'idade': request.form['idade'], 
        'sexo': request.form['sexo'],
        'localidade': request.form['localidade'],
        'telefone': request.form['telefone'],
        'email': request.form['email'],
        'especialidade': request.form['especialidade'],
     
        #'idAgenda': request.form[idAngeda], 
        #'idAvaliacao': request.from['idAvaliacao']
    })

    return redirect(url_for('index'))

@app.route('/profissionais', methods=['GET', 'POST'])
def findAll():
    list_collection  = collection.find()
    return render_template('/main/profissional/list.html', profissionais = list_collection )    

@app.route('/profissionais/<id>')
def findOne(id):
    data = collection.find_one({
        "_id": ObjectId(id)
    })
    return render_template('/main/profissional/viewProfisisonal.html', profissional = data)

@app.route('/profissionais/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    data = collection.delete_many({
        "_id": ObjectId(id)
    })
    
    return redirect(url_for('findAll'))




#rotas cliente
@app.route('/cliente')
def indexCliente():
    return render_template('main/home.html')


#endrotas

if __name__ == '__main__':
    app.run()