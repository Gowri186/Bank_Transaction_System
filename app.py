from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="bank_db"
    )

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- BANK ----------------
@app.route('/bank', methods=['POST'])
def create_bank():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO bank (code, name, address) VALUES (%s, %s, %s)",
            (data['code'], data['name'], data['address'])
        )
        db.commit()
        return jsonify({"message": "Bank created"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        db.close()


# ---------------- BRANCH ----------------
@app.route('/branch', methods=['POST'])
def create_branch():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO branch (branch_id, name, address, bank_code) VALUES (%s, %s, %s, %s)",
            (data['branch_id'], data['name'], data['address'], data['bank_code'])
        )
        db.commit()
        return jsonify({"message": "Branch created"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        db.close()


# ---------------- CUSTOMER ----------------
@app.route('/customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO customer (custid, name, address, phone) VALUES (%s, %s, %s, %s)",
            (data['custid'], data['name'], data['address'], data['phone'])
        )
        db.commit()
        return jsonify({"message": "Customer created"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        db.close()


# ---------------- ACCOUNT ----------------
@app.route('/account', methods=['POST'])
def create_account():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            """INSERT INTO account (account_no, acc_type, balance, branch_id, custid)
               VALUES (%s, %s, %s, %s, %s)""",
            (
                data['account_no'],
                data['acc_type'],
                data['balance'],
                data['branch_id'],
                data['custid']
            )
        )
        db.commit()
        return jsonify({"message": "Account created"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        db.close()


# ---------------- TRANSACTION ----------------
@app.route('/transaction', methods=['POST'])
def transaction():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT balance FROM account WHERE account_no=%s",
            (data['account_no'],)
        )
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Account not found"})

        balance = float(result['balance'])
        amount = float(data['amount'])

        if data['type'] == "withdrawal":
            if balance < amount:
                return jsonify({"error": "Insufficient balance"})
            new_balance = balance - amount
        else:
            new_balance = balance + amount

        # update account
        cursor.execute(
            "UPDATE account SET balance=%s WHERE account_no=%s",
            (new_balance, data['account_no'])
        )

        # insert transaction
        cursor.execute(
            """INSERT INTO transactions (account_no, type, amount, balance)
               VALUES (%s, %s, %s, %s)""",
            (data['account_no'], data['type'], amount, new_balance)
        )

        db.commit()

        return jsonify({
            "message": "Transaction successful",
            "balance": new_balance
        })

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        db.close()


# ---------------- DROPDOWN DATA (IMPORTANT) ----------------
@app.route('/banks')
def get_banks():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bank")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(data)


@app.route('/branches')
def get_branches():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM branch")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(data)


@app.route('/customers')
def get_customers():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customer")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(data)


@app.route('/accounts')
def get_accounts():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM account")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(data)


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)

