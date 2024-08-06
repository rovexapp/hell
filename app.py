from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/api/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'user_id': user[0], 'clicks': user[1], 'invites': user[2], 'currency': user[3]})
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/update_user', methods=['POST'])
def update_user():
    data = request.json
    user_id = data.get('user_id')
    clicks = data.get('clicks')
    invites = data.get('invites')
    currency = data.get('currency')

    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE users SET clicks = ?, invites = ?, currency = ? WHERE user_id = ?''',
                   (clicks, invites, currency, user_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
