
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///security_requests.db'
db = SQLAlchemy(app)

# Initialize Slack client
slack_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
SECURITY_CHANNEL = os.getenv('SLACK_CHANNEL_ID')

class SecurityRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    requester = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/requests', methods=['POST'])
def create_request():
    data = request.json
    new_request = SecurityRequest(
        request_type=data['type'],
        description=data['description'],
        requester=data['requester']
    )
    db.session.add(new_request)
    db.session.commit()

    # Send Slack notification
    try:
        message = f"New Security Request\nType: {data['type']}\nRequester: {data['requester']}\nDescription: {data['description']}"
        slack_client.chat_postMessage(channel=SECURITY_CHANNEL, text=message)
    except SlackApiError as e:
        print(f"Error sending slack message: {e}")

    return jsonify({"id": new_request.id}), 201

@app.route('/api/requests', methods=['GET'])
def get_requests():
    requests = SecurityRequest.query.all()
    return jsonify([{
        'id': r.id,
        'type': r.request_type,
        'description': r.description,
        'status': r.status,
        'requester': r.requester,
        'created_at': r.created_at.isoformat()
    } for r in requests])

@app.route('/api/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    req = SecurityRequest.query.get_or_404(request_id)
    data = request.json
    req.status = data['status']
    db.session.commit()
    return jsonify({"status": "updated"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
