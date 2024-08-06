from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/api/trade', methods=['POST'])
def trade_currency():
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
        action = data.get('action')  # "buy" or "sell"

    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT currency FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_currency = user[0]

    if action == "buy":
        # Assume 1 USDT = 1000 HELLO (for simplicity)
        usdt_to_hello = amount * 1000
        cursor.execute('UPDATE users SET currency = currency + ? WHERE user_id = ?', (usdt_to_hello, user_id))
    elif action == "sell":
        hello_to_usdt = amount / 1000
        if user_currency < amount:
            return jsonify({'error': 'Insufficient HELLO balance'}), 400
        cursor.execute('UPDATE users SET currency = currency - ? WHERE user_id = ?', (amount, user_id))
        # Here you would integrate with an actual payment gateway to transfer USDT to the user

    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
