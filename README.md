🏆 Scorekeeper API

A Flask-based Leaderboard API with JWT Authentication, Caching, and SQLite Database.
This project allows users to register, login, submit scores, view leaderboards, and check ranks.

-------------------------------------------------------------------------

🚀 Features

✅ User Authentication

Register new users with hashed passwords

Secure login using JWT tokens

✅ Score Management

Submit or update a player’s score

Automatically keeps the highest score for each player

✅ Leaderboard

Top 10 players ranked by score

Cached leaderboard for faster responses

✅ Rank System

Fetch a specific player’s rank among all players

✅ Caching

Leaderboard is cached for 30 seconds using Flask-Caching

-------------------------------------------------------------------------

🛠️ Tech Stack

Backend Framework: Flask (Python)

Database: SQLite (SQLAlchemy ORM)

Authentication: JWT (flask-jwt-extended)

Security: Werkzeug Password Hashing

Caching: Flask-Caching

------------------------------------------------------------------------
📦 Installation

Clone the repository

git clone https://github.com/VaishuSidhu/scorekeeper-api.git
cd scorekeeper-api

-----------------------------------------------------------------------
Create and activate a virtual environment

python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate


Install dependencies

pip install -r requirements.txt


Run the app

python app.py


The server will start at:

http://127.0.0.1:5000

🔑 API Endpoints

---------------------------------------------------------------------

📝 Example Workflow

Register → Create an account

Login → Get JWT token

Submit Score → Post your score with the token

View Leaderboard → See top 10 players

Check Rank → Find your rank globally

--------------------------------------------------------------------

📚 Requirements

Python 3.8+

Flask

Flask-JWT-Extended

Flask-Caching

Flask-SQLAlchemy

Install them using:

pip install flask flask-jwt-extended flask-caching flask-sqlalchemy

--------------------------------------------------------------------

🌟 Future Enhancements

Real-time leaderboard updates using WebSockets (Flask-SocketIO)

Role-based access (Admin vs Player)

Achievements & badges for milestones

Daily/Weekly leaderboards


👨‍💻 Author
Developed by Vaishnavy ✨


🏆 Scorekeeper API

A clean and simple Trader Leaderboard API built with Flask, SQLite, and JWT authentication.
It manages trader scores, generates a dynamic leaderboard, and secures updates with authentication.

🚀 Features

🔐 User Authentication with JWT

👤 Register/Login system with hashed passwords

📊 Leaderboard API – Top 10 traders ranked by score

🏅 Rank API – Check rank & score for any trader

⚡ Caching for fast leaderboard retrieval (30s cache)

🗂 SQLite database for persistence

🛠 Tech Stack

Backend: Flask (Python)

Database: SQLite (via SQLAlchemy ORM)

Auth: JWT (flask_jwt_extended)

Cache: Flask-Caching (SimpleCache)

📂 Project Structure
scorekeeperAPI/
│── app.py               # Main application
│── leaderboard.db       # SQLite database (auto-created)
│── venv/                # Virtual environment (recommended)
│── requirements.txt     # Dependencies
│── README.md            # Documentation

⚙️ Setup Instructions

1️⃣ Clone the repository

git clone https://github.com/VaishuSidhu/ScorekeeperAPI.git
cd scorekeeperAPI


2️⃣ Create and activate virtual environment

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


3️⃣ Install dependencies

pip install -r requirements.txt


4️⃣ Run the app

python app.py


5️⃣ Server will start at:
👉 http://127.0.0.1:5000/

📦 Requirements

Create a requirements.txt with:

Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Flask-Caching
Werkzeug

🔑 Authentication Flow

Register → Create account via /register.

Login → Get JWT token via /login.

Use Token → Add token to Authorization header when posting scores:

Authorization: Bearer <your_token>
API Endpoints
1️⃣ Register User (POST /register)
2️⃣ Login User(POST /login)
3️⃣ Add/Update Trader Score (🔒 Protected)(POST /api/scores)
Headers:
4️⃣ Get Leaderboard (GET /api/leaderboard)

🏅 Bonus Features

✅ JWT authentication on score updates

✅ Passwords hashed with Werkzeug

✅ Leaderboard cached for 30s

👨‍💻 Author

Vaishnavy S 

Scorekeeper API – Developed for a backend recruitment challenge.

📜 License

This project is licensed under the MIT License.
MIT License

Copyright (c) 2025 Vaishnavy_04

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
