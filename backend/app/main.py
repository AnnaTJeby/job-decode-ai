from fastapi import FastAPI
app=FastAPI()
@app.get("/")
def home():
    return {
        "message": "Welcome to JobDecode AI Backend!"
    }
@app.get("/hello")
def hello():
    return {
        "message": "Hello from FastAPI!"
    }