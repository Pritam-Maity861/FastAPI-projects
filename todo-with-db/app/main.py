from fastapi import FastAPI

app=FastAPI(
    title="Todo with db connection"
)

@app.get("/root")
async def root():
    return {
        "message":"This is root path"
    }