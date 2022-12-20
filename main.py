import os
from dotenv import load_dotenv
import uvicorn


"""
This main file and we have to run this file and this application
runs on uvicorn server on 8000 port.
"""

load_dotenv()


if __name__ == "__main__":   
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    uvicorn.run("server.app:app", host=host, port=int(port), lifespan="on")
