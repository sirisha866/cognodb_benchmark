import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

uri = os.getenv("COGNODB_URI")
username = os.getenv("COGNODB_USER")
password = os.getenv("COGNODB_PASSWORD")

if not uri or not username or not password:
    raise RuntimeError(
        "Set COGNODB_URI, COGNODB_USER, and COGNODB_PASSWORD in .env first."
    )

driver = GraphDatabase.driver(uri, auth=(username, password))
try:
    with driver.session() as session:
        result = session.run(
            """
            CREATE (a:Person {name: 'Alice'})
            CREATE (b:Person {name: 'Bob'})
            CREATE (a)-[:KNOWS]->(b)
            RETURN a.name AS person, b.name AS friend
            """
        )
        for record in result:
            print(record["person"], "knows", record["friend"])
finally:
    driver.close()