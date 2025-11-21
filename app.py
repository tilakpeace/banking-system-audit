from flask import Flask, request, jsonify
import uuid
from typing import Dict, Any
from datetime import datetime
import hashlib
import json

app = Flask(__name__)

# In-memory event store
events = []
accounts_snapshot = {}


class BankAccount:
    def __init__(self, account_id: str, customer_name: str, initial_balance: float = 0):
        self.account_id = account_id
        self.customer_name = customer_name
        self.balance = initial_balance
        self.status = 'active'
        self.transactions = []
        self.created_at = datetime.now()


    def deposit(self, amount: float, description: str):
        self.balance += amount
        self.transactions.append({
            'type': 'deposit',
            'amount': amount,
            'description': description,
            'timestamp': datetime.now(),
            'balance_after': self.balance
        })

    def withdraw(self, amount: float, description: str):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transactions.append({
            'type': 'withdrawal', 
            'amount': amount,
            'description': description,
            'timestamp': datetime.now(),
            'balance_after': self.balance
        })

    def close(self, reason: str):
        self.status = 'closed'

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'customer_name': self.customer_name,
            'balance': self.balance,
            'status': self.status,
            'transaction_count': len(self.transactions),
            'transactions': self.transactions,
            'created_at': self.created_at.isoformat()
        }

    def to_checksum_dict(self):
        """Returns a deterministic representation for checksum calculation"""
        return {
            'account_id': self.account_id,
            'customer_name': self.customer_name,
            'balance': round(self.balance, 2),  # Round to avoid floating point issues
            'status': self.status,
            'transaction_count': len(self.transactions)
        }




def create_event(event_type: str, account_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new event"""
    event = {
        'event_id': str(uuid.uuid4()),
        'event_type': event_type,
        'account_id': account_id,
        'data': data,
        'timestamp': datetime.now().isoformat(),
    }
    
    events.append(event)
    return event


def apply_event(event: Dict[str, Any]):
    """Apply event to current state"""
    event_type = event['event_type']
    account_id = event['account_id']
    data = event['data']
    
    if event_type == 'account_opened':
        account = BankAccount(
            account_id=account_id,
            customer_name=data['customer_name'],
            initial_balance=data.get('initial_balance', 0)
        )
        accounts_snapshot[account_id] = account

        
    elif event_type == 'funds_deposited':
        account = accounts_snapshot.get(account_id)
        if account.status == 'active':
            account.deposit(data['amount'], data.get('description'))
            
    elif event_type == 'funds_withdrawn':
        account = accounts_snapshot.get(account_id)
        if account.status == 'active':
            account.withdraw(data['amount'], data.get('description'))
            
    elif event_type == 'account_closed':
        account = accounts_snapshot.get(account_id)
        if account:
            account.close(data.get('reason', ''))


def calculate_events_checksum() -> str:
    """Calculate checksum of all events for verification"""
    # Create deterministic representation of events
    events_data = []
    for event in sorted(events, key=lambda x: x['timestamp']):
        events_data.append({
            'event_type': event['event_type'],
            'account_id': event['account_id'],
            'data': event['data'],
            'timestamp': event['timestamp']
        })
    
    events_string = json.dumps(events_data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(events_string.encode('utf-8')).hexdigest()

def calculate_checksum(accounts_data: Dict[str, Any]) -> str:
    """Calculate SHA-256 checksum of accounts state"""
    # Create a deterministic string representation
    accounts_list = []
    for account_id in sorted(accounts_data.keys()):
        account = accounts_data[account_id]
        accounts_list.append(account.to_checksum_dict())
    
    state_string = json.dumps(accounts_list, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(state_string.encode('utf-8')).hexdigest()



def replay_events() -> Dict[str, Any]:
    """Replay all events to rebuild current state"""
    global accounts_snapshot
    accounts_snapshot = {}

    print(f"Replaying {len(events)} events...")
    
    # Store events checksum before replay
    events_checksum = calculate_events_checksum()

    for event in sorted(events, key=lambda x: x['timestamp']):
        apply_event(event)

    # Calculate state checksum after replay
    state_checksum = calculate_checksum(accounts_snapshot)
    
    print(f"Replay complete - {len(accounts_snapshot)} accounts rebuilt")


    return {
        'accounts_rebuilt': len(accounts_snapshot),
        'state_checksum': state_checksum,
        'events_checksum': events_checksum
    }


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
    try:
            data=request.get_json()

            account_id = str(uuid.uuid4())[:8]  # Short ID for demo


            event = create_event(
                "account_opened",
                account_id,
                {
                    'customer_name': data.get('customer_name', 'Unknown'),
                    'initial_balance': float(0),
                    # 'account_type': data.get('account_type', 'checking')
                }
            )

            apply_event(event)

            return jsonify(
                {
                    'message':'Account opened successfully',
                    'account_id':account_id,
                    'balance':accounts_snapshot[account_id].balance

                }
            ),201



    except Exception as e:
        return jsonify({"error":str(e)}),400    



@app.route('/accounts/<account_id>/deposit',methods=['POST'] )
def deposit(account_id):
    try:
        data = request.get_json()
        amount = float(data['amount'])

        # Check if account is not opened
        if account_id not in accounts_snapshot:
            return jsonify({'error': 'Account not found'}), 404
        
        # Check if account is closed or not
        if accounts_snapshot[account_id].status != 'active':
            return jsonify({'error': 'Account is not active'}), 400

        event = create_event(
            'funds_deposited',
            account_id,
            {
                'amount': amount,
                'description': data.get('description', 'Deposit')
            }
        )

        apply_event(event)
        
        return jsonify({
            'message': 'Deposit successful',
            'account_id': account_id,
            'amount': amount,
            'new_balance': accounts_snapshot[account_id].balance
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400




@app.route('/accounts/<account_id>/withdraw',methods=['POST'] )
def withdraw(account_id):

    try:
        data = request.get_json()
        amount = float(data['amount'])
        
        # Check if account is not opened
        if account_id not in accounts_snapshot:
            return jsonify({'error': 'Account not found'}), 404
        
        # Check if account is closed or not
        if accounts_snapshot[account_id].status != 'active':
            return jsonify({'error': 'Account is not active'}), 400
        
        # Verifying sufficient balance
        if amount > accounts_snapshot[account_id].balance:
            return jsonify({'error': 'Insufficient funds'}), 400
        
        event = create_event(
            'funds_withdrawn',
            account_id,
            {
                'amount': amount,
                'description': data.get('description', 'Withdrawal')
            }
        )
        
        apply_event(event)
        
        return jsonify({
            'message': 'Withdrawal successful',
            'account_id': account_id,
            'amount': amount,
            'new_balance': accounts_snapshot[account_id].balance
        })

        


    except Exception as e:
        return jsonify({'error': str(e)}), 400
        

@app.route('/accounts/<account_id>/transfer',methods=['POST'] )
def transfer(account_id):
    try:
        data = request.get_json()
        from_account = account_id
        to_account = data['to_account_id']
        amount = float(data['amount'])
        

        # Check if source account is not opened
        if from_account not in accounts_snapshot:
            return jsonify({'error': 'Source account not found'}), 404

        # Check if destination account is not opened
        if to_account not in accounts_snapshot:
            return jsonify({'error': 'Destination account not found'}), 404
            
        from_acc = accounts_snapshot[from_account]
        to_acc = accounts_snapshot[to_account]
        
        # Check if account is closed or not
        if from_acc.status != 'active' or to_acc.status != 'active':
            return jsonify({'error': 'One or both accounts are not active'}), 400
        
        # Checking sufficient balance
        if amount > from_acc.balance:
            return jsonify({'error': 'Insufficient funds for transfer'}), 400
        
        transfer_id = str(uuid.uuid4())
        
        event_transfer_from=create_event(
            'funds_withdrawn',
            from_account,
            {
                'amount': amount,
                'description': f"Transfer to {to_account}",
                'transfer_id': transfer_id
            }
        )
        
        apply_event(event_transfer_from)

        event_transfer_to=create_event(
            'funds_deposited',
            to_account,
            {
                'amount': amount,
                'description': f"Transfer from {from_account}",
                'transfer_id': transfer_id
            }
        )

        apply_event(event_transfer_to)

        return jsonify({
            'message': 'Transfer successful',
            'transfer_id': transfer_id,
            'amount': amount,
            'from_account_balance': accounts_snapshot[from_account].balance,
            'to_account_balance': accounts_snapshot[to_account].balance
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400



@app.route('/accounts/<account_id>/close',methods=['POST'] )
def close(account_id):
    try:
        if account_id not in accounts_snapshot:
            return jsonify({'error': 'Account not found'}), 404
            
        account = accounts_snapshot[account_id]
        if account.status == 'closed':
            return jsonify({'error': 'Account already closed'}), 400
        
        event = create_event(
            'account_closed',
            account_id,
            {
                'final_balance': account.balance,
                'reason': request.get_json().get('reason', 'Customer request')
            }
        )
        
        apply_event(event)
        
        return jsonify({
            'message': 'Account closed successfully',
            'account_id': account_id,
            'final_balance': account.balance
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/accounts/<account_id>' )
def get_account(account_id):
    if account_id not in accounts_snapshot:
        return jsonify({'error': 'Account not found'}), 404
        
    account = accounts_snapshot[account_id]
    return jsonify(account.to_dict())


@app.route('/accounts' )
def list_accounts():
    accounts_list = {acc_id: acc.to_dict() for acc_id, acc in accounts_snapshot.items()}
    return jsonify({
        'total_accounts': len(accounts_list),
        'accounts': accounts_list
    })

@app.route('/events' )
def get_eventss():
    return jsonify({
        'total_events': len(events),
        'events': events
    })



@app.route('/replay', methods=['POST'] )
def replay():
    try:
        accounts_before = len(accounts_snapshot)
        result=replay_events()
        
        return jsonify({
            'message': 'Event replay completed successfully',
            'events_processed': len(events),
            'accounts_rebuilt': len(accounts_snapshot),
            'accounts_before': accounts_before,
            'accounts_after': len(accounts_snapshot),
            'accounts_rebuilt': result['accounts_rebuilt'],

            'state_checksum': result['state_checksum'],
            'events_checksum': result['events_checksum'],
            'verification': 'Identical checksums across replays confirm determinism'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500




if __name__ == "__main__":
    app.run(debug=True, port=5000)

