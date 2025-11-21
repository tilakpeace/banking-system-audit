from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return """

    <h1>MVP - Banking System Audit</h1>
    <h3>Endpoints:</h3>
    <ul>
        <li><b>POST /accounts/open</b> - Open new account</li>
        <li><b>POST /accounts/&lt;id&gt;/deposit</b> - Deposit funds</li>
        <li><b>POST /accounts/&lt;id&gt;/withdraw</b> - Withdraw funds</li>
        <li><b>POST /transfer</b> - Transfer between accounts</li>
        <li><b>POST /accounts/&lt;id&gt;/close</b> - Close account</li>
        <li><b>GET /accounts/&lt;id&gt;</b> - Get account info</li>

        <li><b>GET /accounts</b> - List all accounts</li>
        <li><b>GET /events</b> - View all events</li>
        <li><b>POST /replay</b> - Replay all events</li>

    </ul>

"""


@app.route('/accounts/open',methods=['POST'] )
def open_account():
    return "test"

@app.route('/accounts/<account_id>/deposit',methods=['POST'] )
def deposit(account_id):
    print(account_id)
    return "test"

@app.route('/accounts/<account_id>/withdraw',methods=['POST'] )
def withdraw(account_id):
    print(account_id)
    return "test"

@app.route('/accounts/<account_id>/transfer',methods=['POST'] )
def transfer(account_id):
    print(account_id)
    return "test"

@app.route('/accounts/<account_id>/close',methods=['POST'] )
def close(account_id):
    print(account_id)
    return "test"


@app.route('/accounts/<account_id>' )
def get_account(account_id):
    print(account_id)
    return "test"


@app.route('/accounts' )
def list_accounts():
    return "test"

@app.route('/events' )
def get_eventss():
    return "test"



@app.route('/replay', methods=['POST'] )
def replay():
    return "test"



if __name__ == "__main__":
    app.run(debug=True, port=5000)

