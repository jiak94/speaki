from fastapi import FastAPI

app = FastAPI()


@app.get("/echo")
async def echo():
    return {"msg": "Hello World"}
