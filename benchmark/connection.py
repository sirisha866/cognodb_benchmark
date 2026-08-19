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

driver = GraphDatabase.driver(
    uri,
    auth=(username, password)
)

try:
    driver.verify_connectivity()
    print("Successfully connected to CognoDB!")
finally:
    driver.close()