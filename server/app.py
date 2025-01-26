from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():

    if request.method == 'GET':
        mess = []
        for message in Message.query.order_by(Message.created_at.asc()).all():
            message_dict = message.to_dict()
            mess.append(message_dict)
        response = make_response(mess, 200)
        return response

        
    elif request.method == 'POST':
        new_message = Message(
            body=request.json["body"],
            username=request.json["username"]
        )
        db.session.add(new_message)
        db.session.commit()

        response = make_response(new_message.to_dict(), 201)
        return response
    
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)

    if not message:
        return make_response(jsonify({"error": "Message not found"}), 404)

    data = request.get_json()
    if "body" in data:
        message.body = data["body"]

    db.session.commit()
    
    return make_response(jsonify(message.to_dict()), 200)


@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)

    if not message:
        return make_response(jsonify({"error": "Message not found"}), 404)

    db.session.delete(message)
    db.session.commit()

    return make_response(jsonify({"message": "Message deleted"}), 204)


if __name__ == '__main__':
    app.run(port=5555)