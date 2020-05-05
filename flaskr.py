from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient, DESCENDING, ASCENDING
from bson.objectid import ObjectId
from bson import json_util
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
tb_solicitacao = conn.solicitacao
############################


#_cadastra novo cliente
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

#_List clients
@app.route('/clients', methods=['GET', 'POST'])
def findAllClients():
    bd_response  = collection_cliente.find()
    if bd_response:
        result   = []
        for i in bd_response:
            result.append(i)

        result = json.loads(json_util.dumps(result))
        return jsonify(result=result),200
    else:
        return jsonify(result="error")

#_seta perfil cliente
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


#_seta mentor cliente
@app.route('/cliente/mentores/<id>', methods = ['POST'])
def get_mentores(id):

    bd_response = collection_cliente.aggregate([
    {
        '$match': {
            "_id": ObjectId(id)
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


#_desvincula profissional de cliente
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

#_vincula profissional ao cliente
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


#_Create new profissional
@app.route('/profissionais/create',  methods=['GET', 'POST'])
def create():
    bd_response = collection.insert_one({
        'nome': request.form['nome'],
        'idade': request.form['idade'],
        'sexo': request.form['sexo'],
        'localidade': request.form['localidade'],
        'telefone': request.form['telefone'],
        'email': request.form['email'],
        'especialidade': request.form['especialidade'],
    })
    
    if bd_response:
       
        return jsonify(result="sucess"),200
    else:
        return jsonify(result="error")




#_List professionals
@app.route('/profissionais', methods=['GET', 'POST'])
def findAll():
    bd_response  = collection.find()
    if bd_response:
        result   = []
        for i in bd_response:
            result.append(i)

        result = json.loads(json_util.dumps(result))
        return jsonify(result=result),200
    else:
        return jsonify(result="error")

#_Searching for a professional by ID
@app.route('/profissionais/<id>', methods=['GET', 'POST'])
def findOne(id):
    data = collection.find_one({
        "_id": ObjectId(id)
    })
    if bd_response:
        page_sanitized = json.loads(json_util.dumps(bd_response))
        return jsonify(result=page_sanitized),200
    else:
        return jsonify(result="error")

#_Searching client by email
@app.route('/cliente/<email>', methods=['GET', 'POST'])
def findOne_by_email(email):
    bd_response = collection_cliente.find_one({
        "email": email
    })
    
    if bd_response:
        page_sanitized = json.loads(json_util.dumps(bd_response))
        return jsonify(result=page_sanitized),200
    else:
        return jsonify(result="error")

#_Exclude one professional By ID
@app.route('/profissionais/delete/<id>', methods=['GET', 'POST', 'DELETE'])
def delete(id):
    bd_response = collection.delete_many({
        "_id": ObjectId(id)
    })
    if bd_response:
        
        return jsonify(result="sucess"),200
    else:
        return jsonify(result="error")


#_Show a profissional to edition
@app.route('/profissionais/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    data = collection.find_one({
        "_id": ObjectId(id)
    })
    if bd_response:
        page_sanitized = json.loads(json_util.dumps(bd_response))
        return jsonify(result=page_sanitized),200
    else:
        return jsonify(result="error")

#_Edit a profissional By ID
@app.route('/profissionais/update/<id>', methods=['GET', 'POST', 'PUT'])
def update(id):
    bd_response = collection.update_one({
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
    if bd_response:
        return jsonify(result="sucess"),200
    else:
        return jsonify(result="error")

###########
#_Create professional assessment
@app.route('/profissinais/newRating',  methods=['GET', 'POST'])
def createCliente():
    bd_response = tb_avaliacao.insert_one({
        'idPorfissional': 3,
        'idCliente': 3,
        'rating': 7
    })
    if bd_response:
       return jsonify(result="sucess"),200
    else:
       return jsonify(result="error")

###########


############################
#Others route


#_HOME's route
@app.route('/profissionais/home', methods = ['GET'])
def home():
    #Consulta par exibir todas os mais bem avaliados
    profissionais = tb_avaliacao.find().sort("rating", DESCENDING).limit(4)
    if bd_response:
        result   = []
        for i in bd_response:
            result.append(i)

        result = json.loads(json_util.dumps(result))
        return jsonify(result=result),200
    else:
        return jsonify(result="error")



#_Route to save schedule
@app.route('/profissionais/agenda/save', methods = ['GET', 'POST'])
def saveAgenda():
    bd_response= tb_agenda.insert_one({
        'idPorfissional': 1,
        'clientesAgendados': {
            'idCliente': 1,
            'horario_inicio': request.form['horario_inicio'],
            'horario_fim': request.form['horario_fim'],
        }
    })
    if bd_response:
        return jsonify(result="sucess"),200
    else:
        return jsonify(result="error")
    


#_Route to edit schedule
@app.route('/profissionais/agenda/edit/<id>', methods=['GET', 'POST'])
def editAgenda(id):
    bd_response = collection.find_one({
        "_id": ObjectId(id)
    })
    return render_template('/main/profissional/editAgenda.html', profissional = data)
    if bd_response:
        page_sanitized = json.loads(json_util.dumps(bd_response))
        return jsonify(result=page_sanitized),200
    else:
        return jsonify(result="error")

#_Route to update schedule
@app.route('/profissionais/agenda/update', methods = ['GET', 'POST', 'PUT'])
def updateAgenda(id):
    bd_response = tb_agenda.update_one(
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
    if bd_response:
        
        return jsonify(result="sucess"),200
    else:
        return jsonify(result="error")

#_Exclude a professional's schedule By ID
@app.route('/profissionais/agenda/delete/<id>', methods=['GET', 'POST', 'DELETE'])
def deleteAgenda(id):
    bd_response = tb_agenda.delete_many({
        "_id": ObjectId(id)
    })

    if bd_response:
        page_sanitized = json.loads(json_util.dumps(bd_response))
        return jsonify(result=page_sanitized),200
    else:
        return jsonify(result="error")
    
#_Professional send request to client 
@app.route('/solicitacao/nova', methods=['GET', 'POST'])
def solicitarMentoria():
    response = request.args
    bd_response = tb_solicitacao.insert_one({
        'idProfissional': response['idProfissional'],
        'idCliente': response['idCliente'],
        'status': response['status'],
    })

    if bd_response:
        #page_sanitized = json.loads(json_util.dumps(bd_response))
        return jsonify(result="sucess"),200
    else:
        return jsonify(result="error")


#_Professional reject request to client 
@app.route('/solicitacao/rejeitar/<id>', methods=['GET', 'POST', 'DELETE'])
def rejeitarMentoria(id):
    #response = request.args
    bd_response = tb_solicitacao.delete_many({
        "_id": ObjectId(id)
    })

    if bd_response:
        #page_sanitized = json.loads(json_util.dumps(bd_response))
        return jsonify(result="sucess"),200
    else:
        return jsonify(result="error")

#_Professional acept request to client 
@app.route('/solicitacao/aceitar/<id>', methods=['GET', 'POST', 'PUT'])
def aceitarMentoria(id):
    response = request.args
    bd_response = tb_solicitacao.update_one(
        {'_id': ObjectId(id)},
        {
            '$set':{
                'status': response['status'],
            }
        }
    )

    if bd_response:
        #page_sanitized = json.loads(json_util.dumps(bd_response))
        return jsonify(result="sucess"),200
    else:
        return jsonify(result="error")


#_Search requests actives
@app.route('/solicitacao/findByActives/<id>', methods=['GET', 'POST'])
def editSolicitacao(id):
    bd_response = tb_solicitacao.find_one({
        "_id": ObjectId(id)
    })
    if bd_response:
        #page_sanitized = json.loads(json_util.dumps(bd_response))
        return jsonify(result="Sucess"),200
    else:
        return jsonify(result="error")


#endrotas
if __name__ == '__main__':
    app.debug = True
    app.run( host = st.HOST,port = st.PORT)
