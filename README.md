# address_book
A simple, clean  Address Book Application built using FastAPI, SQLAlchemy, and SQLite.
This application allows users to:

✔ Create, update, delete addresses
✔ Validate latitude & longitude
✔ Store data in SQLite
✔ Search addresses within distance (using Haversine formula)
✔ Use clean, modular architecture for production readiness
✔ Test the entire API through pytest

# 🚀 Tech Stack

FastAPI – Fast Python web framework

Pydantic – Data validation

SQLAlchemy ORM – Database ORM

SQLite – Simple lightweight database

# 📦 Project Structure
├── __init__.py
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── utils.py
├── decorators.py
├── Dockerfile
└── README.md


# 📥 Installation**

1. Clone Repository
git clone <your_repo_url>
cd address-book-api

2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Install Requirements
pip install -r requirements.txt


# ▶️ Run the Application direclty**
uvicorn main:app --reload


The API will be available at:

👉 http://127.0.0.1:5000

Swagger Docs:

👉 http://127.0.0.1:5000/docs


# 🐳 Run Application Using Docker**

This project includes a Dockerfile so you can run the entire FastAPI app in a container without installing Python or dependencies on your machine.

✅ 1. Build Docker Image

Run this command from the project root (where the Dockerfile is located):

docker build -t address-book-api .

Explanation:

docker build → builds the Docker image

-t address-book-api → names the image

. → uses current directory as build context

✅ 2. Run the Docker Container
docker run -d -p 5000:5000 --name address-book-container address-book-api

Explanation:

-d → run container in background

-p 5000:5000 → map local port 5000 to container port 5000

--name address-book-container → name for easy management

address-book-api → name of the image you built

✅ 3. Verify the Application Is Running

Open the browser and visit:

👉 http://localhost:5000

Swagger UI:

👉 http://localhost:5000/docs

# 🛠 Useful Docker Commands**

Stop the container

docker stop address-book-container

Start again

docker start address-book-container

View logs

docker logs address-book-container

Remove container

docker rm -f address-book-container

Remove image
docker rmi address-book-api

