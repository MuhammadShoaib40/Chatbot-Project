from flask import Flask, render_template, request, session, redirect, url_for
from neo4j import GraphDatabase
import openai
from pyaiml21 import Kernel
from glob import glob
import nltk
from nltk.corpus import wordnet
import wikipedia
from pyDatalog import pyDatalog
import requests
from bs4 import BeautifulSoup
import pickle

bot_name="Shaun"

app = Flask(__name__)
app.secret_key = 'Shoaib94'

# Configure your OpenAI API credentials
openai.api_key = 'sk-...5yuZ'

# Configure Neo4j driver
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Allahis1"))

myBot = Kernel()




aimls = glob("./data/*.aiml")
for aiml_file in aimls:
    myBot.learn(aiml_file)

print('All files learned')

myBot.respond('set name Shoaib', '0')
myBot.setPredicate('name', 'Shoaib', sessionID='0')

# Download required NLTK resources
nltk.download('punkt')
nltk.download('wordnet')

# User credentials (username: password)
user_credentials = {
    'Shoaib': {'password': 'Allahis1', 'name': 'Shoaib'},
    'Ali': {'password': 'alliswell', 'name': 'Ali'},
    'Bob': {'password': 'password', 'name': 'Bob Johnson'}
}





def save_brain_dump(data):
    try:
        with open('brain_dump.pickle', 'wb') as file:
            pickle.dump(data, file)
        return True
    except Exception as e:
        print(f"An error occurred while saving the brain dump: {str(e)}")
        return False

def load_brain_dump():
    try:
        with open('brain_dump.pickle', 'rb') as file:
            data = pickle.load(file)
        return data
    except Exception as e:
        print(f"An error occurred while loading the brain dump: {str(e)}")
        return {}




def fetch_information(data):
    try:
        summary = wikipedia.summary(data)
        return f"{data}: {summary[:200]}..."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Please provide more specific information about {data}."
    except wikipedia.exceptions.PageError as e:
        return f"Sorry, I couldn't find information about {data} on Wikipedia."

# Usage example: Fetch information about Python programming language
data = "Python programming language"
information = fetch_information(data)
print(information)

def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Customize the web scraping logic based on the structure of the website
        # Extract the desired information from the HTML content
        # Return the scraped information

        # Example: Scrape information about a person from a specific website
        # Modify the logic to match the structure of the target website
        name = soup.find('h1', {'class': 'person-name'}).get_text()
        occupation = soup.find('span', {'class': 'occupation'}).get_text()
        scraped_data = f"Name: {name}\nOccupation: {occupation}"

        return scraped_data
    except requests.exceptions.RequestException as e:
        return "Error occurred during web scraping"

def create_node(tx, label, properties):
    query = f"CREATE (n:{label} $properties)"
    tx.run(query, properties=properties)

def create_relation(tx, start_node, relation, end_node):
    query = """
    MATCH (a), (b)
    WHERE a.name = $start_node AND b.name = $end_node
    CREATE (a)-[:`{relation}`]->(b)
    """
    tx.run(query, start_node=start_node, end_node=end_node, relation=relation)



def create_user_node(tx, name):
    query = "CREATE (u:User {name: $name})"
    tx.run(query, name=name)

@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        name = session.get('name', '')
        return render_template('index.html', username=username, name=name)
    else:
        return redirect(url_for('login'))


def login_user(username):
    session['username'] = username
    session['name'] = user_credentials[username]['name']

    # Create a user node in Neo4j
    try:
        with driver.session() as neo4j_session:
            neo4j_session.write_transaction(create_user_node, session['name'])

        # Save user information in the brain dump
        brain_dump = load_brain_dump()
        if 'users' not in brain_dump:
            brain_dump['users'] = {}
        brain_dump['users'][username] = {'name': session['name']}
        save_brain_dump(brain_dump)

    except Exception as e:
        print(f"An error occurred while creating a user node: {str(e)}")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in user_credentials and user_credentials[username]['password'] == password:
            login_user(username)

            return redirect(url_for('home'))

        else:
            # Incorrect password or user does not exist
            return render_template('error.html', message='Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']

        if username and password and name:
            if username not in user_credentials:
                # Create a new user with the provided credentials
                user_credentials[username] = {'password': password, 'name': name}

                # Create a user node in Neo4j
                with driver.session() as neo4j_session:
                    neo4j_session.write_transaction(create_user_node, name)

                return redirect(url_for('login'))
            else:
                # User already exists
                return render_template('error.html', message='Username already exists')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect(url_for('login'))

@app.route('/get_response', methods=['GET', 'POST'])
def get_response():
    fetch_information(data)
    if request.method == 'POST':
        user_input = request.json['user_input']

        if user_input.lower() in ['bye', 'goodbye', 'see you', 'see you next time']:
            return 'Goodbye!'

        # Check if the user wants to log out
        if user_input.lower() in ['logout', 'sign out']:
            return redirect(url_for('logout'))

            # Handle "who are you" question
        if user_input.lower() in ['who are you', 'what is your name']:
            return f" I am {bot_name}, your chatbot assistant!"
        if user_input.lower() in ['who created you', 'who made you? ','whp is your botmaster? ']:
            return " Shoaib created me, He is my Botmaster!"



        if user_input.lower() == 'tell me a joke':
            return "Why don't scientists trust atoms? Because they make up everything!"

        if user_input.lower() == 'what is the capital of France?':
            return "The capital of France is Paris."

        # Add more custom queries and responses based on your requirements

        # Process user input with NLTK WordNet
        tokens = nltk.word_tokenize(user_input)
        synonyms = []
        for token in tokens:
            synsets = wordnet.synsets(token)
            for synset in synsets:
                synonyms.extend(synset.lemmas())

        response = myBot.respond(user_input, '0')
        asked_about = myBot.get_predicate('what', '0')
        if asked_about != 'unknown':
            # Fetch information using OpenAI API
            information = fetch_information(asked_about)
            response = f"{asked_about}: {information}"
            myBot.respond('remove what predicate', '0')

            # Create nodes and relations in Neo4j
            with driver.session() as session:
                session.write_transaction(create_node, "User", {"name": "Shoaib"})
                session.write_transaction(create_node, "Topic", {"name": asked_about})
                session.write_transaction(create_relation, "Shoaib", "ASKED_ABOUT", asked_about)
                session.commit()

        # Web scraping example
        if user_input.startswith('scrape'):
            _, _, url = user_input.split(' ')
            scraped_data = scrape_website(url)
            return scraped_data

        return response

    return 'Invalid request'

if __name__ == '__main__':
    app.run(port=5001)