from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="bank_db"
    )

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def create_account():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO accounts (account_no, name, branch, balance) VALUES (%s,%s,%s,%s)",
            (data['account_no'], data['name'], data['branch'], data['balance'])
        )
        db.commit()
        return jsonify({"message": "Account Created"})
    except Exception as e:
        db.rollback()
        return jsonify({"message": str(e)})
    finally:
        cursor.close()
        db.close()


@app.route('/transaction', methods=['POST'])
def transaction():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT balance FROM accounts WHERE account_no=%s", (data['account_no'],))
        result = cursor.fetchone()

        if not result:
            return jsonify({"message": "Account not found"})

        balance = float(result['balance'])
        amount = float(data['amount'])

        if data['type'] == "withdrawal":
            if balance < amount:
                return jsonify({"message": "Insufficient Balance"})
            new_balance = balance - amount
        else:
            new_balance = balance + amount

        cursor.execute(
            "UPDATE accounts SET balance=%s WHERE account_no=%s",
            (new_balance, data['account_no'])
        )

        cursor.execute(
            "INSERT INTO transactions (account_no, type, amount, balance) VALUES (%s,%s,%s,%s)",
            (data['account_no'], data['type'], amount, new_balance)
        )

        db.commit()

        return jsonify({
            "message": "Transaction Successful",
            "balance": new_balance
        })

    except Exception as e:
        db.rollback()
        return jsonify({"message": str(e)})

    finally:
        cursor.close()
        db.close()


@app.route('/transactions')
def get_transactions():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)