# Web API 🪛

Client - Server communicate with Request and Response.

## Curl

Tool used to make request to WebServer specifing:

- Request
- Header
- Data

Alternative: Postman

## Request Uri:

Uri is basically a link containing:

- path: location of the resources
- query string: parameters

## Request Method:

- GET : get a resource.
- POST : create new data.
- PUT/PATCH: update all attribute or update just a subset.
- DELETE: delete a resource.

## Request Header

Information about the request.
Format (json) Authorization Token, Connection Time, Response Accepted Format.

## Request Body

Other specific information and Data.

## Response Codes:

+200: OK
+400: Error in Client Side
+500: Error in Server Side

# FastAPI ⚡

Why this tool?
Similar to NodeJS and Go.

- Asynchronous Server: Handle a lot of requests in a single process.
- Easy: to use and learn.
- Short: minimize code duplication.
- Robust: production ready code.
- Standard Base: OpenAPI + JSON Schema (Help to auto-generate Docs)

## Pydantic: Modern Data Validation in Python

Classes and Data-Classes (optimized for holding information with utilities)

- Pydentic let us create Data-Classes with <b>Validators</b>. Validators are useful in order to be sure that the request is Valid (but can be used also for response)

- Validate Sensitive Values (like in .env)

Example of validator:

        from pydantic import BaseModel
        class User_validator(BaseModel):
            id:int
            name = 'John Doe'
            signup_ts: Optional[datetime] = None
            friends: List[int] = []
        
This class allow us to create User in such way each istance of this class can be validate by pydantic.

ValidationError can be catched using:

        try { #
         build our pydentic data class 
        }
        except ValidationError as e:
            print(e)

The printing will show what went wrong in validate the class.

# Installation FastAPI 💾

        pip install "fastapi[all]"

## Getting Started

        # Simple Get Request
        @app.get("/") # Path Operation Decorator
        def root(): # Path Operation Function
            #Simple Response to Get Request
            return { "message: Hello! you are in the root!" }

## Running the server 🖥️

use <b> uvicorn </b> library in order to start a server.

        univorn server.py:app --reload

we can find auto-generated doc in http://126.0.0.1:8000

- /openapi.json 
- /docs
- /redoc

Response can be:

- dict
- list
- singular value 
- pydentic models

## Path Parameters: parameter for identify resources

Example:

        @app.get("/items/{item_id}")
        def read_item(item_id: int)

<b>NB: if we don't specify {item_id} than the parameter is considered as query parameters. Query params refers on the way we want to process the resources </b>

## Request Body

        class Item(BaseModel)
        ...
        @app.post("/items/")
        def create_item(item: Item):
            return item
        
        # item: Item is a parameter declared as class Item

# Pratice with FastAPI

import HTTPstatus library.

Create a file called api.py and:

- create: app = FastAPI(...infos)
- create response/request using @construct_response decorator
- return an accepted object

### RPC style: invoke procedures from Client via HTTP
### REST style: endopoint are named with name of entity

TAGS: @app.get("/", tags=["Name"]) tags help our auto-doc to track this request or responses

TIP: message, status-code and data are field that a response must have

Verify that all is ok:
- Start server
- Make requests with Curl