from fastapi.testclient import TestClient
from utils import read_id

from server import app
client = TestClient(app)

# testare che dando un immagine
def test_prediction():
    image_file = '../../data/processed/arcDatasetSelected/Achaemenid architecture/21_Tonbeaux-achemenides.JPG'
    files = {'imgfile': ('21_Tonbeaux-achemenides.JPG', open(image_file, 'rb'))}
    response = client.post("/predict/", files=files)
    nuovo_id = read_id()
    assert response.status_code == 200
    assert response.json() == {"filename": '21_Tonbeaux-achemenides.JPG', "id": str(nuovo_id-1), "label": 'ancient egyptian architecture'}
