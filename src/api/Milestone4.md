# API for classification

## Requirements

        pip install "fastapi[all]"
        pip install "uvicorn[standard]"
        pip install python-multipart

## Endpoints

### Classificazione di immagini:

- /uploadimage/: accetta un file immagine e restituisce la classificazione.
  - Per poterla utilizzare avviare send_file.py