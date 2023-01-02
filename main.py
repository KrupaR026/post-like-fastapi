import os
from dotenv import load_dotenv
import uvicorn


"""
This is main file and we can run it on uvicorn server port 8000.
"""

load_dotenv()


if __name__ == "__main__":
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    uvicorn.run("server.app:app", host=host, port=int(port), lifespan="on")
