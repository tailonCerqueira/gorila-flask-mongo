from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient, DESCENDING, ASCENDING
from bson.objectid import ObjectId

app = Flask(__name__)

#Conection With database
client      = MongoClient('localhost', 27017)
conn        = client['app_gorila']

############################
#Instantiation of documents collections
collection  = conn.profissional
tb_avaliacao = conn.avaliacao
tb_agenda = conn.agenda
############################

#Redirec to register professional
@app.route('/profissionais/new', methods = ['GET', 'POST'])
def new():
     return render_template('/main/profissional/new.html')

#Register new professional
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

#List professionals
@app.route('/profissionais', methods=['GET', 'POST'])
def findAll():
    list_collection  = collection.find()
    return render_template('/main/profissional/list.html', profissionais = list_collection )    

#Searching for a professional by ID
@app.route('/profissionais/<id>', methods=['GET', 'POST'])
def findOne(id):
    data = collection.find_one({
        "_id": ObjectId(id)
    })
    return render_template('/main/profissional/viewProfisisonal.html', profissional = data)

#Exclude one professional By ID
@app.route('/profissionais/delete/<id>', methods=['GET', 'POST', 'DELETE'])
def delete(id):
    data = collection.delete_many({
        "_id": ObjectId(id)
    })
    
    return redirect(url_for('findAll'))

#exibir um profissional para edição
@app.route('/profissionais/edit/<id>', methods=['GET', 'POST', 'PUT'])
def edit(id):
    data = collection.find_one({
        "_id": ObjectId(id)
    })
    return render_template('/main/profissional/edit.html', profissional = data)

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
#Create professional assessment
@app.route('/profissinais/newRating',  methods=['GET', 'POST'])
def createCliente():
    tb_avaliacao.insert_one({
        'idPorfissional': 3,
        'idCliente': 3, 
        'rating': 7
    })

    return redirect(url_for('index'))
###########

#Redirect to Clinet's register
@app.route('/cliente/new', methods = ['GET', 'POST'])
def newCliente():
     return render_template('/main/cliente/new.html')

############################
#Others route

############################
#Route to create Login's screen
@app.route('/', methods = ['GET'])
def index():
    return render_template('/main/login.html')

#Route HOME
@app.route('/profissionais/home', methods = ['GET'])
def home():
    #Consulta par exibir todas os mais bem avaliados
    profissionais = tb_avaliacao.find().sort("rating", DESCENDING).limit(4)
    return render_template('/main/profissional/home.html', profissionais_by_rating = profissionais)

############################
############################
#Agend's route
@app.route('/profissionais/agenda', methods = ['GET', 'POST'])
def agenda():
    return render_template('/main/profissional/agenda.html')

#Route to create schedule
@app.route('/profissionais/agenda/new', methods = ['GET', 'POST'])
def newAgenda():
    return render_template('/main/profissional/newAgenda.html')

#Route to save schedule
@app.route('/profissionais/agenda/save', methods = ['GET', 'POST'])
def saveAgenda():
    tb_agenda.insert_one({
        'idPorfissional': 1,
        'clientesAgendados': {
            'idCliente': 1,
            'horario_inicio': request.form['horario_inicio'],
            'horario_fim': request.form['horario_fim'],
        }
    })
    return redirect(url_for('home'))

#Route to edit schedule
@app.route('/profissionais/agenda/edit/<id>', methods=['GET', 'POST'])
def editAgenda(id):
    data = collection.find_one({
        "_id": ObjectId(id)
    })
    return render_template('/main/profissional/editAgenda.html', profissional = data)

#Route to update schedule
@app.route('/profissionais/agenda/update', methods = ['GET', 'POST', 'PUT'])
def updateAgenda(id):
    tb_agenda.update_one(
        {'_id': ObjectId(id)},
        {
            '$set':{
                'clientesAgendados': {
                    'horario_inicio': request.form['horario_inicio'],
                    'horario_fim': request.form['horario_fim'],
                }
            }
        }
    )
    return redirect(url_for('home'))

#Exclude a professional By ID
@app.route('/profissionais/agenda/delete/<id>', methods=['GET', 'POST', 'DELETE'])
def deleteAgenda(id):
    data = tb_agenda.delete_many({
        "_id": ObjectId(id)
    })
    
    return redirect(url_for('findAll'))


#ENDROUTES
if __name__ == '__main__':
    app.run()