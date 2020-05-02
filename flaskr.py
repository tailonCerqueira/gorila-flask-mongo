from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient, DESCENDING, ASCENDING
from bson.objectid import ObjectId

app = Flask(__name__)

#Conexão com o banco
client      = MongoClient('localhost', 27017)
conn        = client['app_gorila']

############################
#instanciação do documento
collection  = conn.profissional
tb_avaliacao = conn.avaliacao
############################

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
    })

    return redirect(url_for('index'))

#lista profissionais
@app.route('/profissionais', methods=['GET', 'POST'])
def findAll():
    list_collection  = collection.find()
    return render_template('/main/profissional/list.html', profissionais = list_collection )    

#busca um profissional por ID
@app.route('/profissionais/<id>', methods=['GET', 'POST'])
def findOne(id):
    data = collection.find_one({
        "_id": ObjectId(id)
    })
    return render_template('/main/profissional/viewProfisisonal.html', profissional = data)

#excluir um profissional por ID
@app.route('/profissionais/delete/<id>', methods=['GET', 'POST', 'DELETE'])
def delete(id):
    data = collection.delete_many({
        "_id": ObjectId(id)
    })
    
    return redirect(url_for('findAll'))

#exibir um profissional para edição
@app.route('/profissionais/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    data = collection.find_one({
        "_id": ObjectId(id)
    })
    return render_template('/main/profissional/edit.html', profissional = data)

#editar um profissional por ID
@app.route('/profissionais/update/<id>', methods=['GET', 'POST', 'PUT'])
def update(id):
    collection.update_one({
            "_id": ObjectId(id)
        },
        {
            '$set':{
                'nome': request.form['nome'],
                'idade': request.form['idade'], 
                'sexo': request.form['sexo'],
                'localidade': request.form['localidade'],
                'telefone': request.form['telefone'],
                'email': request.form['email'],
                'especialidade': request.form['especialidade'],     
            }        
        }        
    )    

    return redirect(url_for('findAll'))
###########  
###########
###########
#criar avaliacao profissional
@app.route('/profissinais/newRating',  methods=['GET', 'POST'])
def createCliente():
    tb_avaliacao.insert_one({
        'idPorfissional': 3,
        'idCliente': 3, 
        'rating': 7
    })

    return redirect(url_for('index'))
###########

#redirecionar para cadastro de cliente
@app.route('/cliente/new', methods = ['GET', 'POST'])
def newCliente():
     return render_template('/main/cliente/new.html')

############################
#outras rotass

############################
#rota para a tela de login
@app.route('/', methods = ['GET'])
def index():
    return render_template('/main/login.html')

#rota home
@app.route('/profissionais/home', methods = ['GET'])
def home():
    #Consulta par exibir todas os mais bem avaliados
    profissionais = tb_avaliacao.find().sort("rating", DESCENDING).limit(4)
    return render_template('/main/profissional/home.html', profissionais_by_rating = profissionais)



#endrotas

if __name__ == '__main__':
    app.run()