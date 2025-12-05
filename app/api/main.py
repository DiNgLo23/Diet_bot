from fastapi import FastAPI
from app.api.routers import users, food

app = FastAPI()


app.include_router(users.router)
app.include_router(food.router)


@app.get("/")
def read_root():
    return {"message": "None"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

