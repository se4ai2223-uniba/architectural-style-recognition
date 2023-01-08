# ML system design 🔧

## 1. 💻 Model Inference Function 

At this time, we have already trained the model and built the APIs.

- Input of the model: feature vector
- Output of the model: prediction with label, number, boolean ...

### 1.1 👨 Allow the user to interact with the model

Is all about "architectural decision" that describe **what are the main components and how they communicate with each other.**

The architectural decisions affect non-functional parts of the system

- Latency, Scalability, Privacy, Cost, Complexity...

*Example: we want handle n users in our system then it is needed to know how to do that* 

### 1.2 Feature Encoding

Deciding where the encording of features is made (in Model Infernence time or outside this step) ?

### 1.3 Feature Store

Goal: reuse features across models and projects by storing them in different sets used for different purposes, different models etc...

- Feature Set A: features given by SQL query
- Feature Set B: features taken by a .csv file

Some platform are: Feast, Tecton, AWS sage Maker Feature Store (in order to NOT built feature store from scratch)

### 1.4 Where to deploy the model? Server-side or Client-side


#### 1.4.1 Server (Popular)
We want that the model is in remote so we have to assume:

- User send request (Network Latency)
- Server receive the request
- Server perform computation 
- User get the results

**Ways to send data** <br>
- Batch Prosessing: process multiple and fixed amounts of data in a single payload. (Asynchronus)
- Stream Processing: process data that continuously is given in input (for example taken by cams) (Asynchronus)
- Real-Time Processing: Single input (like in our case) (Synchronus since we aspect to not exceed Time Out of the server).

#### 1.4.2 Users

- User send request
- Local request
- The device of the user do the computation (Processing Latency)
- User get the result

the model is compiled in the system or can be built in JavaScript if it is assumed that the user has internet connection.