from flask import Flask, request, jsonify
from flask_pymongo import pymongo, ObjectId
#Permite interactuar el servidor de react con el server de python
from flask_cors import CORS

CONNECTION_STRING = "mongodb+srv://vas:CenA,.-3218@cluster0.poxub.mongodb.net/<dbname>?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')
user_collection = pymongo.collection.Collection(db, 'user_collection')
#test to insert data to the data base

app = Flask(__name__)

@app.route('/')
def flask_mongodb_atlas():
    return "flask mongodb atlas!"


@app.route('/users', methods=['POST'])
def createUser():
    id = db.users.insert({
        'name': request.json['name'],
        'email': request.json['email'],
        'calle': request.json ['calle'],
        'passwd': request.json['passwd']
    })
    print(str(ObjectId(id)))
    return jsonify(str(ObjectId(id)))

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.users.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'passwd': doc['passwd']
        })
    return jsonify(users)

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    print(user)
    return jsonify({
        '_id': str(ObjectId((user['_id']))),
        'name': user['name'],
        'email': user['email'],
        'passwd': user['passwd']
    })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    db.users.delete_one({'_id': ObjectId(id)})
    return "usuario eliminado"

@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
    db.users.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'email': request.json['email'],
        'passwd': request.json['passwd']
    }})
    return jsonify({'msg': 'user updated'})

@app.route("/test")
def test():
    db.collection.insert_one({"name": "Pepe"})
    return "Connected to the data base!"


if __name__ == '__main__':
    app.run(debug=True)