# Durhack2023 - Data Pipeline for Premier League Predictor - Table 7

## Marshall Wace Task: Data Pipeline for Predicting Premier League Game Scores

Welcome to our predictive analytics project developed during Durhack2023 by Team 7. Our system employs a data pipeline coupled with a machine learning model to predict the outcomes of Premier League football matches with high accuracy.

### Team Members:

- Mateusz Radzikowski
- Vidadi Nasibov
- Harshvardhan Patil
- Mohammad Reza Sharifi

## Project Overview

Our solution is built with a microservices architecture that includes the following components:

- **Message Broker (RabbitMQ):** Manages the message queue for asynchronous task processing, coordinating the flow between publishers and consumers.

- **Backend Service (FastAPI):** Offers a high-performance API, encapsulating the logic for interfacing with the machine learning model and database.

- **Data Publishers and Consumers (Python):** Scripts designed to collect, preprocess, and manage the flow of data to and from the database, using RabbitMQ for task queuing.

- **Database (PostgreSQL):** A central repository for storing processed data that powers the backend predictions.

- **Machine Learning Model (Random Forest Regressor with Python):** The predictive engine, hosted within the FastAPI backend, predicts the scores based on the incoming data.

- **Frontend Application (React):** A user-friendly interface that displays upcoming fixtures and historical data along with the predicted scores, allowing users to evaluate the model's performance.

## Prerequisites

Before starting, make sure you have the following installed:

- Docker and Docker Compose.
- Git (to clone the repository).
- Ensure that local ports 3000 for frontend and 8080 backend are free.
- The local port for data injector (publisher) - 8082
- The local port for data processor (consumer) - 8081
- The local port for database PostgreSQL - 5432

## Installation and Setup

To get the project up and running:

```bash
git clone https://github.com/mradzikowski/Durhack2023.git
cd Durhack2023
```