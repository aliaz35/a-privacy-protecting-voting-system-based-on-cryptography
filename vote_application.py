from flask import Flask, request, jsonify

app = Flask(__name__)

votes = {
    "候选人1": 0,
    "候选人2": 0,
    "候选人3": 0
}

@app.route('/')
def index():
    return app.send_static_file('vote.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    vote = data.get("vote")
    key = data.get("key")
    if vote in votes:
        votes[vote] += 1
        return jsonify({"message": "投票成功", "votes": votes})
    else:
        return jsonify({"message": "无效的投票选项"}), 400

if __name__ == '__main__':
    app.run(ssl_context="adhoc", debug=True)
