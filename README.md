#  Bank Transaction Management System

##  Overview

A full-stack web application that simulates core banking operations such as account creation, deposits, withdrawals, and transaction tracking.

Built to demonstrate **DBMS concepts and real-world system integration** 
---

##  Features 

* Create and manage banks, branches, and customers
* Open accounts with different types
* Deposit and withdraw money with validation
* Real-time balance updates
* Transaction history tracking
* Dynamic dropdowns (auto-fetch data)
* Clear and refresh functionality

---

##  Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python (Flask)
* **Database:** MySQL
* **Connector:** mysql-connector-python

---

##  Project Structure

```
Bank_Transaction_System/
│
├── app.py
├── templates/
│   └── index.html
└── README.md
```

---

##  Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/
cd Bank_Transaction_System
```

### 2. Install dependencies

```
pip install flask mysql-connector-python
```

### 3. Configure Database

Update credentials inside `app.py`:

```
host="localhost"
user="root"
password="root123"
database="bank_db"
```

---

## 🗄️ Database Schema

```
CREATE DATABASE bank_db;
USE bank_db;

CREATE TABLE bank (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(200)
);

CREATE TABLE branch (
    branch_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(200),
    bank_code VARCHAR(10),
    FOREIGN KEY (bank_code) REFERENCES bank(code)
);

CREATE TABLE customer (
    custid VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(200),
    phone VARCHAR(15)
);

CREATE TABLE account (
    account_no VARCHAR(20) PRIMARY KEY,
    acc_type VARCHAR(20),
    balance DECIMAL(15,2),
    branch_id VARCHAR(10),
    custid VARCHAR(10),
    FOREIGN KEY (branch_id) REFERENCES branch(branch_id),
    FOREIGN KEY (custid) REFERENCES customer(custid)
);

CREATE TABLE transactions (
    txn_id INT AUTO_INCREMENT PRIMARY KEY,
    account_no VARCHAR(20),
    type VARCHAR(20),
    amount DECIMAL(15,2),
    balance DECIMAL(15,2),
    txn_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_no) REFERENCES account(account_no)
);
```

---

##  Run the Application

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

##  Demo

https://drive.google.com/file/d/1Pt9Hiik6XjbajJo152o08dL7XPZjM7sz/view?usp=sharing

##  Key Concepts Implemented

* Relational Database Design
* Primary and Foreign Keys
* Data Integrity and Constraints
* Transaction Handling
* REST API Integration

---

##  Notes

* This is a simplified banking system for learning purposes
* No authentication or security layer implemented
