#  Bank Transaction System

##  Overview
This project is a **Bank Transaction Management System** built using a full-stack approach. It allows users to create accounts, perform deposits and withdrawals, and view transaction history. The system demonstrates integration between frontend, backend, and database components.

---

##  Technologies Used
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **Database:** MySQL  
- **Connector:** mysql-connector-python  

---

##  Features
- Create new bank accounts  
- Deposit money  
- Withdraw money with balance validation  
- View transaction history  
- Real-time balance updates  
- Clear/reset form functionality  

---

##  Project Structure

Bank_Transaction_system_dbms
│
├── app.py
├── templates/
│ └── index.html
└── README.md


---

##  Video 
Watch the working demo of the project here:



https://github.com/user-attachments/assets/f1cff034-ae88-4426-99e7-d15f5ada2914

---

##  Database Setup
Run the following SQL commands:

```sql
CREATE DATABASE bank_db;
USE bank_db;

CREATE TABLE accounts (
    account_no INT PRIMARY KEY,
    name VARCHAR(100),
    branch VARCHAR(100),
    balance DECIMAL(10,2)
);

CREATE TABLE transactions (
    txn_id INT AUTO_INCREMENT PRIMARY KEY,
    account_no INT,
    type ENUM('deposit','withdrawal'),
    amount DECIMAL(10,2),
    balance DECIMAL(10,2),
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_no) REFERENCES accounts(account_no)
);

---














