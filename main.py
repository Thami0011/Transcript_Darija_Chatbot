import uvicorn

if __name__ == "__main__":
    # Run the FastAPI app
    uvicorn.run("Controller.Controller:app", host= "127.0.0.1", port = 8000, reload = False)