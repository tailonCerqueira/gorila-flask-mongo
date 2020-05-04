from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient, DESCENDING, ASCENDING
from bson.objectid import ObjectId
import settings as st
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)
#Conection With database
client      = MongoClient(st.DB_URL, int(st.DB_PORT))
conn        = client[st.DB_COLLECTION]

############################
#Instantiation of documents collections
collection  = conn.profissional
collection_cliente  = conn.cliente
tb_avaliacao = conn.avaliacao
tb_agenda = conn.agenda
############################




#cadastra novo cliente
@app.route('/cliente/create', methods = ['GET','POST'])
def new_cliente():
    response = request.args
    bd_response = collection_cliente.insert_one({
        'nome': response['nome'],
        'idade': response['idade'],
        'sexo': response['sexo'],
        'localidade': response['localidade'],
        'telefone': response['telefone'],
        'email': response['email'],
        'path_imagem': response['path_image'],
        'perfil_investimento': response['perfil']
    })

    if bd_response:
        return jsonify(result="created"),201
    else:
        return jsonify(result="error")


#seta perfil cliente
@app.route('/cliente/set/perfil', methods = ['POST'])
def cliente_set_perfil():
    response = request.args
    bd_response = collection_cliente.update_one({

    "_id": ObjectId(response['id'])
        },{
              '$set': {
                      'perfil_investimento':response['perfil'].lower()
                        }
              }, upsert=False)

    if bd_response:
        return jsonify(result="sucess"),200
    else:
        return jsonify(result="error")


#seta mentor cliente
@app.route('/cliente/mentores/<id>', methods = ['POST'])
def get_mentores(id):

    bd_response = collection_cliente.aggregate([
    {
        '$match': {
            'nome': 'goku'
        }
    }, {
        '$lookup': {
            'from': 'profissional',
            'localField': 'perfil_investimento',
            'foreignField': 'especialidade',
            'as': 'perfil_compativel'
        }
    }, {
        '$project': {
            '_id': 0,
            'nome': 0,
            'idade': 0,
            'sexo': 0,
            'localidade': 0,
            'telefone': 0,
            'email': 0,
            'path_imagem': 0,
            'perfil_investimento': 0
        }
    }
    ])
    if bd_response:
        result   = []
        for i in bd_response:
            result.append(i)

        result = json.loads(json_util.dumps(result))
        return jsonify(result=result),200
    else:
        return jsonify(result="error")


#desvincula profissional de cliente
@app.route('/cliente/remover/profissional/<id>', methods = ['GET','POST'])
def cliente_remove_profissional(id):
    bd_response = collection_cliente.update_one({
            "_id": ObjectId(id)
        },{
              '$unset': {
                      'idProfissional': ""
                        }
              }, upsert=False)
    if bd_response:
        return jsonify(result="removed"),200
    else:
        return jsonify(result="error")

#vincula profissional ao cliente
@app.route('/cliente/<id_cliente>/adicionar/profissional/<id_profissional>', methods = ['GET','POST'])
def cliente_adicionar_profissional(id_cliente,id_profissional):
    bd_response = collection_cliente.update_one({
            "_id": ObjectId(id_cliente)
        },{
              '$set': {
                      'id_profissional':id_profissional
                        }
              }, upsert=False)
    if bd_response:
        return jsonify(result="sucess"),200
    else:
        return jsonify(result="error")

#Register new professional
@app.route('/profissionais/new', methods = ['GET', 'POST'])
def new():
     return render_template('/main/profissional/new.html')

#Create new profissional
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

#Show a profissional to edition
@app.route('/profissionais/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    data = collection.find_one({
        "_id": ObjectId(id)
    })
    return render_template('/main/profissional/edit.html', profissional = data)

#Edit a profissional By ID
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

#HOME's route
@app.route('/profissionais/home', methods = ['GET'])
def home():
    #Consulta par exibir todas os mais bem avaliados
    profissionais = tb_avaliacao.find().sort("rating", DESCENDING).limit(4)
    return render_template('/main/profissional/home.html', profissionais_by_rating = profissionais)

#Schedule's route
@app.route('/profissionais/agenda', methods = ['GET'])
def agenda():
    return render_template('/main/profissional/agenda.html')

#Route to create schedule
@app.route('/profissionais/agenda/new', methods = ['GET'])
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

#Exclude a professional's schedule By ID
@app.route('/profissionais/agenda/delete/<id>', methods=['GET', 'POST', 'DELETE'])
def deleteAgenda(id):
    data = tb_agenda.delete_many({
        "_id": ObjectId(id)
    })

    return redirect(url_for('findAll'))

#endrotas



if __name__ == '__main__':
    app.debug = True
    app.run( host = st.HOST,port = st.PORT)
