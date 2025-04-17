import uvicorn
"""
This script serves as the entry point for running a FastAPI application using Uvicorn.
Modules:
    uvicorn: ASGI server for running FastAPI applications.
Execution:
    When executed as the main module, this script starts the FastAPI application
    defined in the `app.Controller.Controller` module. The application is hosted
    locally on `127.0.0.1` at port `8000` with the `reload` option disabled.
Usage:
    Run this script directly to start the FastAPI application:
        python main.py
"""

if __name__ == "__main__":
    # Run the FastAPI app
    uvicorn.run("app.Controller.Controller:app", host= "127.0.0.1", port = 8000, reload = False)