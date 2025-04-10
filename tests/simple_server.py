from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.delete("/")
@app.get("/")
@app.head("/")
@app.options("/")
@app.patch("/")
@app.post("/")
@app.put("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=443, ssl_keyfile="key.pem", ssl_certfile="cert.pem"
    )
