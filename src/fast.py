from typing import Any, List
from fastapi import FastAPI
import sqlite3
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os

app = FastAPI()
db = None

@app.post("/sqlite/connect_in_memory")
def create_db_in_memory():
    """
    Create an in-memory SQLite database. If one already exist, it would not recreate. 
    
    returns `{ "connected": True }`
    """
    global db
    if db is not None:
        return {"connected": True}
    try:
        db = sqlite3.connect(":memory:")
        return {"connected": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class QueryRequest(BaseModel):
    query: str
    parameters: List[Any]

@app.post("/sqlite/query")
def parameterized_query(req: QueryRequest):
    """
    Execute a parameterized SQL query on the in-memory SQLite database.

    Provide a JSON payload with sqlite query string and parameters. For example:

    `{ "query": "SELECT ?, ?, ? FROM items", "parameters": [1, "user", 10] }`

      - query: a SQL string containing '?' placeholders
      - parameters: a list of values to substitute in the query
    
    If success, returns a object with `results` property, which is an array of rows (also as array) `{ "results": [[1, "jon", 20], [2, "wig", 10]] }`.

    Otherwise, returns a object with `detail` property showing errors, such as `{ "detail": "near \"string\": syntax error" }`.
    """
    global db
    if db is None:
        raise HTTPException(status_code=400, detail="In-memory SQLite database not created yet. Call /sqlite/connect_in_memory first.")
    try:
        cursor = db.cursor()
        cursor.execute(req.query, req.parameters)
        results = cursor.fetchall()
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class StatusReport(BaseModel):
    connected: bool
    tables: list[str]
    size: int

@app.get("/sqlite/status")
def get_db_status() -> StatusReport:
    """
    Returns the current status of the in-memory SQLite database as a JSON response.

    JSON Response Example:
    `{
        "connected": true,
        "tables": ["table1", "table2"],
        "size": 4096
    }`

    - connected: A boolean indicating if the database connection is active.
    - tables: A list of table names present in the database.
    - size: The size of the database in bytes.
    """
    global db
    if db is None:
        return StatusReport(connected=False, tables=[], size=0)
    try:
        cursor = db.cursor()
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        # Calculate the database size
        cursor.execute("PRAGMA page_count;")
        page_count = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_size;")
        page_size = cursor.fetchone()[0]
        db_size = page_count * page_size  # Size in bytes

        return StatusReport(connected=True, tables=tables, size=db_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/terminate")
def terminate_server(background_tasks: BackgroundTasks):
    """
    Terminates the server after returning a shutdown message.

    Returns:
      A JSON message indicating that the server is shutting down.
    """
    background_tasks.add_task(os._exit, 0)
    return {"message": "Server is shutting down..."}
