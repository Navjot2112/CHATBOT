from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jandu@2003",
        database="chatbot"
    )

# Predefined responses
RESPONSES = {
    "hours": "We are open from 8 AM to 8 PM every day.",
    "location": "We are located at 123 Coffee St, Coffee City.",
    "menu": "We offer a variety of coffees, teas, and snacks. You can view the full menu on our website.",
    "wifi": "Yes, we offer free WiFi to all our customers.",
    "contact": "You can contact us at 9814120047.",
    "greetings": "Hey, how can I assist you today?",
    "farewells": "Alright, have a great day!"
}

# Function to handle queries
def get_response(query):
    query = query.lower()
    if any(word in query for word in ["hours", "time", "open", "close", "business hours"]):
        return RESPONSES["hours"]
    elif any(word in query for word in ["location", "address", "where", "get to"]):
        return RESPONSES["location"]
    elif any(word in query for word in ["menu", "food", "drink", "offer"]):
        return RESPONSES["menu"]
    elif any(word in query for word in ["wifi", "internet", "wi-fi"]):
        return RESPONSES["wifi"]
    elif any(word in query for word in ["contact", "phone", "reach", "number"]):
        return RESPONSES["contact"]
    elif any(word in query for word in ["hi", "hello", "hey"]):
        return RESPONSES["greetings"]
    elif any(word in query for word in ["bye", "ok", "goodbye", "thanks", "thank you"]):
        return RESPONSES["farewells"]
    else:
        return "I'm sorry, I don't understand your question."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def chatbot_response():
    try:
        user_text = request.form['msg']
        bot_response = get_response(user_text)

        # Insert user message and bot response into the database
        db_connection = get_db_connection()
        mycursor = db_connection.cursor()
        sql = "INSERT INTO entries (user_message, bot_response) VALUES (%s, %s)"
        val = (user_text, bot_response)
        mycursor.execute(sql, val)
        db_connection.commit()
        
        # Close the cursor and the database connection
        mycursor.close()
        db_connection.close()

        return jsonify(bot_response)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify("There was an error. Please try again.")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
