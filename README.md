# House Price Prediction API

[![CI Pipeline](https://github.com/mliang4/housing-deploy/actions/workflows/ci.yml/badge.svg)](https://github.com/mliang4/housing-deploy/actions/workflows/ci.yml)

This project is a machine learning-powered REST API that predicts house prices based on the California Housing dataset. It is built with **FastAPI** and **Scikit-learn**, and is containerized with **Docker** for easy deployment on platforms like **Render**.

## 🚀 Features

*   **Machine Learning Model**: Uses a Linear Regression model trained on the California Housing dataset.
*   **FastAPI**: High-performance, easy-to-use web framework for building APIs.
*   **Automated Training**: The model is retrained automatically during the Docker build process, ensuring the deployment always uses a fresh model.
*   **Dockerized**: Fully containerized application for consistent environments.

## 🛠️ Tech Stack

*   **Python 3.10+**
*   **FastAPI** (Web Framework)
*   **Scikit-learn** (Machine Learning)
*   **Pandas** (Data Manipulation)
*   **Docker** (Containerization)

## 📂 Project Structure

```
├── src/
│   ├── api.py       # FastAPI application and prediction endpoint
│   ├── train.py     # Script to train and save the model
├── Dockerfile       # Docker configuration for building the image
├── render.yaml      # Render deployment configuration
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

## 🏃‍♂️ Running Locally

1.  **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd housing-deploy
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Train the model**
    This will generate a `models/linear_regression_model.pkl` file.
    ```bash
    python src/train.py
    ```

4.  **Run the API**
    ```bash
    uvicorn src.api:app --reload
    ```

5.  **Test the API**
    Open your browser to `http://127.0.0.1:8000/docs` to see the interactive Swagger UI.

## 📡 API Usage

### Endpoint: `POST /predict`

Predicts the median house value based on input features.

**Request Body:**

```json
{
  "MedInc": 8.3252,
  "AveRooms": 6.9841,
  "AveOccup": 2.5556
}
```

*   `MedInc`: Median Income in block group
*   `AveRooms`: Average number of rooms per household
*   `AveOccup`: Average number of household members

**Response:**

```json
{
  "predicted_house_price": 4.152
}
```

## ☁️ Deployment

This project is configured for deployment on **Render**.

1.  Push your code to GitHub.
2.  Create a new **Blueprint** on Render.
3.  Connect your repository.
4.  Render will automatically detect `render.yaml` and deploy the service.
