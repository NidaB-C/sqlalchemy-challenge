# SurfsUp Climate Analysis

## Overview
The SurfsUp project is a detailed climate analysis using data from Hawaii. The primary goal is to provide insights into Hawaii's weather patterns, particularly focusing on precipitation and temperature observations.

## Project Structure
- `app.py`: A Flask API providing endpoints to query climate data.
- `climate.ipynb`: A Jupyter Notebook containing the detailed climate analysis and data exploration.
- `Resources`: Folder containing the SQLite database with the required datasets.

## Getting Started
To get started with this project, follow these steps:

1. **Clone the Repository**
git clone (https://github.com/NidaB-C/sqlalchemy-challenge) cd SurfsUp

2. **Install Requirements** (Optional)
- It's recommended to create a virtual environment and install the required packages.
python -m venv venv source venv/bin/activate # For Windows, use venv\Scripts\activate pip install -r requirements.txt

3. **Running the Jupyter Notebook**
- Launch Jupyter Notebook to open and run `climate.ipynb` for the climate analysis.
jupyter notebook

4. **Running the Flask API**
- Execute `app.py` to start the Flask API.
python app.py

- Access the API via `http://localhost:5000/` in your web browser.

## API Endpoints
The Flask API provides the following endpoints:
- `/`: The home page listing all available API routes.
- `/api/v1.0/precipitation`: Returns precipitation data for the last year.
- `/api/v1.0/stations`: Lists all weather observation stations.
- `/api/v1.0/tobs`: Shows temperature observations for the most active station for the last year.
- `/api/v1.0/<start>`: Returns temperature summary from a start date.
- `/api/v1.0/<start>/<end>`: Returns temperature summary between start and end dates.

## Technologies Used
- Python
- Flask
- SQLAlchemy
- Jupyter Notebook
- Pandas
- Matplotlib
