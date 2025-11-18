from flask import Flask, request, jsonify, render_template

import datetime

app = Flask(__name__)

transactions = []

@app.route('/api/transactions', methods=['GET', 'POST'])
def request_handler():
    if request.method == 'POST':
        print(f"POSt request have recived: {request.json}")

        transaction_data = request.json.copy()
        transaction_data['received_at'] = datetime.datetime.now().isoformat()
        transaction_data['server_id'] = len(transactions) + 1

        transactions.insert(0, request.json)
        return jsonify({"status": "Success", "message": "OK!"})

    return jsonify({
            'transactions': transactions,
            'count': len(transactions),
            'last_update': datetime.datetime.now().isoformat()
        })

@app.route('/')
def index():
    """Главная страница с таблицей транзакций"""
    return render_template('transactions.html', transactions=transactions)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=8000, debug=True)
