# Chatbot with Flask and Neo4j

This is a simple chatbot application built using Flask web framework and Neo4j graph database. The chatbot leverages the power of AIML (Artificial Intelligence Markup Language) for natural language processing and OpenAI API for retrieving information. It also integrates web scraping capabilities using BeautifulSoup library.

## Features

- User authentication: Users can sign up and log in to the chatbot application.
- AIML-based conversation: The chatbot can respond to user input based on AIML rules.
- Wikipedia integration: The chatbot can fetch information from Wikipedia based on user queries.
- Web scraping: The chatbot can scrape information from specific websites.
- Neo4j integration: The chatbot can create user nodes and relations in Neo4j graph database.

## Prerequisites

Make sure you have the following installed on your machine:

- Python 3
- Flask
- Neo4j
- pyAIML21
- NLTK
- pyswip
- requests
- beautifulsoup4

## Getting Started

1. Clone the repository:


2. Install the required dependencies:


3. Set up the Neo4j database:
- Install Neo4j and start the Neo4j server.
- Modify the Neo4j authentication details in `main.py` to match your Neo4j setup.

4. Configure OpenAI API credentials:
- Sign up for an account and obtain an API key from OpenAI.
- Replace `'sk-...5yuZ'` with your actual OpenAI API key in `main.py`.

5. Run the application:


6. Open your web browser and access `http://localhost:5000` to use the chatbot application.

## Usage

- Sign up with a username, password, and name.
- Log in using your credentials.
- Start a conversation with the chatbot by typing in the input field.
- The chatbot will respond based on the AIML rules and OpenAI API responses.
- You can ask the chatbot questions, request jokes, or perform web scraping by entering specific commands.
- You can also log out at any time.

## Contributions

Contributions to this project are welcome! If you find any issues or want to add new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- The AIML implementation used in this project is based on the [pyAIML21](https://github.com/datenhahn/pyAIML21) library.
- The Flask web framework and Neo4j graph database were used for building the chatbot application.
- NLTK (Natural Language Toolkit) was used for word tokenization and synonym retrieval.
- BeautifulSoup library was used for web scraping.
- OpenAI API was used for retrieving information from Wikipedia.

