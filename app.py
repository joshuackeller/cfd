from flask import Flask, render_template, request, g
from dotenv import load_dotenv
import requests
import psycopg2
from groq import Groq
import os
import json

load_dotenv()

ACCOUNT_ID = "319b04b5f0cf58ae9abe80c086302ea7"
CLOUDFLARE_TOKEN = os.environ.get("CLOUDFLARE_AI_WORKERS_TOKEN")
API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/"
headers = {"Authorization": f"Bearer {CLOUDFLARE_TOKEN}"}


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="password",
            host="localhost",
            port="5432",
        )
    return g.db


@app.before_request
def before_request():
    get_db()


@app.teardown_request
def teardown_request(exception=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template("index.html")


########################## CLOUDFLARE AI WORKERS #############################
@app.route("/api/generate", methods=["POST"])
def generate():
    question = request.get_json().get("question", "")

    result = requests.post(
        f"{API_BASE_URL}@cf/defog/sqlcoder-7b-2",
        headers={"Authorization": f"Bearer {CLOUDFLARE_TOKEN}"},
        json={
            "stream": False,
            "messages": [
                {
                    "role": "user",
                    "content": f"""
### Task
Generate a SQL query to answer [QUESTION]{question}[/QUESTION]

### Database Schema
The query will run on a database with the following schema:
  -- Create table for football teams
  CREATE TABLE team (
      id SERIAL PRIMARY KEY,
      name TEXT NOT null
      );

  -- Create table for game
  CREATE TABLE game (
      id INT PRIMARY KEY,
      home_team_id INT REFERENCES team(id), -- home team for game
      away_team_id INT REFERENCES team(id) -- away team for game
      );

  -- Create table for game result
  CREATE TABLE game_result (
      id SERIAL PRIMARY KEY,
      game_id INT REFERENCES game(id),
      team_id INT REFERENCES team(id),
      points INT NOT NULL, -- points the team scored
      is_winner BOOLEAN, -- boolean that indicates if the team won
      CONSTRAINT unique_game_team UNIQUE (game_id, team_id)
      );

### Answer
Given the database schema, here is the SQL query that [QUESTION]{question}[/QUESTION]
[SQL]
  """,
                },
            ],
        },
    )

    query = result.json()["result"]["response"]

    print("query", query)

    cur = g.db.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    # Convert query results to JSON
    json_data = []
    column_names = [desc[0] for desc in cur.description]

    for row in rows:
        json_data.append(dict(zip(column_names, row)))

    json_data = json.dumps(json_data)

    print("data", json_data)

    cur.close()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
            ### Instructions:
            You will be given a SQL Query, data, and a question. Use the data to answer the question as concisely.
            Don't explain the SQL query. Only use the query to understand the context of the data.
            Assume that the data is directly related to the question. You do not need any more context.
            """,
            },
            {
                "role": "user",
                "content": f"""
                ### Query
                {query}

                ### Data
                {json_data}

                ### Question
                {question}
                """,
            },
        ],
        model="llama3-8b-8192",
    )

    print("chat_completion", chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True)

############################# HUGGING FACE ###################################
# HUGGING_FACE_TOKEN = os.environ.get("HUGGING_FACE_TOKEN")
# @app.route("/api/generate", methods=["POST"])
# def generate():
#     question = request.get_json().get("question", "")

#     API_URL = "https://aer5jazkucifwlp2.us-east-1.aws.endpoints.huggingface.cloud"
#     headers = {
#         "Accept": "application/json",
#         "Authorization": f"Bearer {HUGGING_FACE_TOKEN}",
#         "Content-Type": "application/json",
#     }

#     result = requests.post(
#         API_URL,
#         headers=headers,
#         json={
#             "inputs": f"""
# ### Task
# Generate a SQL query to answer [QUESTION]{question}[/QUESTION]

# ### Database Schema
# The query will run on a database with the following schema:
#   -- Create table for football teams
#   CREATE TABLE team (
#       id SERIAL PRIMARY KEY,
#       name TEXT NOT null
#       );

#   -- Create table for game
#   CREATE TABLE game (
#       id INT PRIMARY KEY,
#       home_team_id INT REFERENCES team(id), -- home team for game
#       away_team_id INT REFERENCES team(id) -- away team for game
#       );

#   -- Create table for game result
#   CREATE TABLE game_result (
#       id SERIAL PRIMARY KEY,
#       game_id INT REFERENCES game(id),
#       team_id INT REFERENCES team(id),
#       points INT NOT NULL, -- points the team scored
#       is_winner BOOLEAN, -- boolean that indicates if the team won
#       CONSTRAINT unique_game_team UNIQUE (game_id, team_id)
#       );

# ### Answer
# Given the database schema, here is the SQL query that [QUESTION]{question}[/QUESTION]
# [SQL]
#   """,
#             "parameters": {
#                 "num_beams": 4,
#                 "do_sample": False,
#                 "return_text": False,
#                 "return_full_text": False,
#                 "return_tensors": False,
#             },
#         },
#     )

#     query = result.json()[0]["generated_text"]

#     print("query", query)

#     cur = g.db.cursor()
#     cur.execute(query)
#     rows = cur.fetchall()

#     # Convert query results to JSON
#     json_data = []
#     column_names = [desc[0] for desc in cur.description]

#     for row in rows:
#         json_data.append(dict(zip(column_names, row)))

#     json_data = json.dumps(json_data)

#     print("data", json_data)

#     cur.close()

#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": """
#             ### Instructions:
#             You will be given a SQL Query, data, and a question. Use the data to answer the question as concisely.
#             Don't explain the SQL query. Only use the query to understand the context of the data.
#             Assume that the data is directly related to the question. You do not need any more context.
#             """,
#             },
#             {
#                 "role": "user",
#                 "content": f"""
#                 ### Query
#                 {query}

#                 ### Data
#                 {json_data}

#                 ### Question
#                 {question}
#                 """,
#             },
#         ],
#         model="llama3-8b-8192",
#     )

#     print("chat_completion", chat_completion.choices[0].message.content)
#     return chat_completion.choices[0].message.content


# if __name__ == "__main__":
#     app.run(debug=True)


################### LOCAL #################################
# @app.route("/api/generate", methods=["POST"])
# def generate():
#     question = request.get_json().get("question", "")


#     result = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "sqlcoder",
#             "stream": False,

#             "prompt": f"""
#   ### Instructions:
#   Your task is to convert a question into a SQL query, given a Postgres database schema.
#   Adhere to these rules:
#   - **Deliberately go through the question and database schema word by word** to appropriately answer the question
#   - **Use Table Aliases** to prevent ambiguity. For example, 'SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id'.
#   - When creating a ratio, always cast the numerator as float

#   ### Input:
#   Generate a SQL query that answers the question `{question}`.
#   This query will run on a database whose schema is represented in this string:
#   -- Create table for football teams
#   CREATE TABLE team (
#       id SERIAL PRIMARY KEY,
#       name TEXT NOT null
#       );

#   -- Create table for game
#   CREATE TABLE game (
#       id INT PRIMARY KEY,
#       home_team_id INT REFERENCES team(id), -- home team for game
#       away_team_id INT REFERENCES team(id) -- away team for game
#       );

#   -- Create table for game result
#   CREATE TABLE game_result (
#       id SERIAL PRIMARY KEY,
#       game_id INT REFERENCES game(id),
#       team_id INT REFERENCES team(id),
#       points INT NOT NULL, -- points the team scored
#       is_winner BOOLEAN, -- boolean that indicates if the team won
#       CONSTRAINT unique_game_team UNIQUE (game_id, team_id)
#       );

#   ### Response:
#   Based on your instructions, here is the SQL query I have generated to answer the question `{question}`:
#   ```sql
#   """,
#         },
#     )
#     response = result.json()["response"]

#     query, ticks = response[:-3], response[-3:]

#     print("query", query)

#     if ticks != "```":
#         raise ValueError("Invalid question")

#     cur = g.db.cursor()
#     cur.execute(query)
#     rows = cur.fetchall()

#     # Convert query results to JSON
#     json_data = []
#     column_names = [desc[0] for desc in cur.description]

#     for row in rows:
#         json_data.append(dict(zip(column_names, row)))

#     json_data = json.dumps(json_data)

#     print("data", json_data)

#     cur.close()

#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": """
#             ### Instructions:
#             You will be given a SQL Query, data, and a question. Use the data to answer the question as concisely.
#             Don't explain the SQL query. Only use the query to understand the context of the data.
#             Assume that the data is directly related to the question. You do not need any more context.
#             """,
#             },
#             {
#                 "role": "user",
#                 "content": f"""
#                 ### Query
#                 {query}

#                 ### Data
#                 {json_data}

#                 ### Question
#                 {question}
#                 """,
#             },
#         ],
#         model="llama3-8b-8192",
#     )

#     print("chat_completion", chat_completion.choices[0].message.content)
#     return chat_completion.choices[0].message.content
