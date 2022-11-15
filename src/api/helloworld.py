from fastapi import FastAPI

app = FastAPI()


from fastapi import FastAPI

app = FastAPI()

# Esempio di path marameters che deve essere per forza un intero
@app.get("/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
