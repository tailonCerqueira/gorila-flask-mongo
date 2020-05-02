from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient, DESCENDING, ASCENDING
from bson.objectid import ObjectId
import settings as st
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
#Conexão com o banco
client      = MongoClient(st.DB_URL, int(st.DB_PORT))
conn        = client[st.DB_COLLECTION]

############################
#instanciação do documento
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

#rota agenda
@app.route('/profissionais/agenda', methods = ['GET'])
def agenda():
    return render_template('/main/profissional/agenda.html')

#rota para criar agenda
@app.route('/profissionais/agenda/new', methods = ['GET'])
def newAgenda():
    return render_template('/main/profissional/newAgenda.html')

#rota para salvar agenda
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

#endrotas

if __name__ == '__main__':
    app.debug = True
    app.run( host = st.HOST,port = st.PORT)
