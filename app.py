from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
from hashlib import sha256
from OnChain.storeInfura import store_data_on_chainn
from OnChain.retriveInfura import get_data_from_transaction
from OnChain.encoding import process_string
from OnChain.decoding import decode_string


app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session management

# Initialize database
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            website_name TEXT,
            url TEXT,
            password_hash TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

# Routes
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = sha256(request.form["password"].encode()).hexdigest()
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return redirect(url_for("home"))
    except sqlite3.IntegrityError:
        return "Username already exists. Try a different one.", 400
    finally:
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = sha256(request.form["password"].encode()).hexdigest()
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session["user_id"] = user[0]
        return redirect(url_for("dashboard"))
    return "Invalid username or password", 403

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("home"))
    return render_template("dashboard.html")

@app.route("/add-website", methods=["POST"])
def add_website():
    if "user_id" not in session:
        return redirect(url_for("home"))

    website_name = request.form["website_name"]
    url = request.form["url"]
    password = request.form["password"]
    encrypted_password = store_in_blockchain(password)  # Store in blockchain
    password_hash = sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO websites (user_id, website_name, url, password_hash)
        VALUES (?, ?, ?, ?)
    """, (session["user_id"], website_name, url, password_hash))
    conn.commit()
    conn.close()

    return redirect(url_for("list_websites"))

@app.route("/websites")
def list_websites():
    if "user_id" not in session:
        return redirect(url_for("home"))

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, website_name, url FROM websites WHERE user_id = ?
    """, (session["user_id"],))
    websites = cursor.fetchall()
    conn.close()

    return render_template("websites.html", websites=websites)

@app.route("/get-password/<int:website_id>")
def get_password(website_id):
    if "user_id" not in session:
        return redirect(url_for("home"))

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT password_hash FROM websites WHERE id = ? AND user_id = ?
    """, (website_id, session["user_id"]))
    website = cursor.fetchone()
    conn.close()

    if not website:
        return "Website not found.", 404

    original_password = retrieve_from_blockchain(website[0])  # Retrieve from blockchain
    return jsonify({"password": original_password})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
