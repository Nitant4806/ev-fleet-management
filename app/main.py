from fastapi import FastAPI


app=FastAPI(
    title="Ev fleet management API ",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message":"Ev fleet API is running"
    }