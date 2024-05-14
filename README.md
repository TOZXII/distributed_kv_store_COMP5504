# Distributed Key-Value Store

This project implements a robust distributed key-value store that facilitates reliable and efficient data management across multiple peer-to-peer (P2P) nodes in a network. The system supports essential operations such as "get", "put", and "delete", allowing for flexible and scalable data storage solutions. The system enhances data availability, fault tolerance.


## Project Structure
```bash
distributed_kv_store/
├── nodes/
│ ├── node.py
│ ├── client.py
│ ├── kvstore.proto
│ ├── init.py
├── proto/
│ ├── kvstore.proto
├── web/
│ ├── app.py
│ ├── templates/
│ │ ├── index.html
│ ├── static/
│ │ ├── style.css
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
```


## Technologies Used

- Python
- gRPC
- LevelDB
- Flask
- Docker
- Docker Compose

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.9 or higher
- Docker
- Docker Compose

### Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/distributed_kv_store.git
cd distributed_kv_store
```

Open Docker application

Set Up the Python Virtual Environment
Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages:
```bash
pip install -r requirements.txt
```

Generate the gRPC code from the proto file:
```bash
python -m grpc_tools.protoc -I./proto --python_out=./nodes --grpc_python_out=./nodes ./proto/kvstore.proto
```

Running the Project
Build and Run the Docker Containers
Build and run the Docker containers using Docker Compose:

```bash
docker-compose build
docker-compose up
```


Usage
Accessing the Web Interface
Open your web browser and navigate to:
```bash
http://localhost:5001
```

Authors
Said Albreiki
Saqer Alshukaili
Jaber Albusaidi
