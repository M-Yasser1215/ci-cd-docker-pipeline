from fastapi import FastAPI

app = FastAPI(title="CI/CD Pipeline Demo")

@app.get("/")
def root():
    return {"status": "ok", "message": "Pipeline is working"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}