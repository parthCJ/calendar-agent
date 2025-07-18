# 💬 TailorTalk: A Conversational AI Appointment Booker

TailorTalk is a sophisticated, conversational AI agent that seamlessly books appointments on a Google Calendar. It features a natural language interface powered by Google Gemini and LangGraph, a robust FastAPI backend, and a user-friendly Streamlit frontend, all containerized with Docker for easy deployment.

## ✨ Features

-   **Natural Conversation:** Engage in a fluid, back-and-forth dialogue to find and book appointments. The agent understands context and asks clarifying questions.
-   **Intelligent Tool Use:** The agent can programmatically check Google Calendar for availability and create new events on the user's behalf.
-   **Stateful Memory:** Remembers the context of the conversation using LangGraph's state management, allowing for complex interactions.
-   **Decoupled Architecture:** A modern full-stack application with a separate frontend and backend, ensuring modularity and scalability.

## 🛠️ Tech Stack

| Component      | Technology            |
| -------------- | --------------------- |
| **Backend** | Python, FastAPI       |
| **Frontend** | Streamlit             |
| **Agent** | LangGraph             |
| **LLM** | Google Gemini Flash   |
| **Database** | Google Calendar API   |
| **Deployment** | Docker, Docker Compose|

## 🚀 How to Run Locally

Follow these steps to set up and run the project on your local machine.

### Prerequisites

-   [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose installed.
-   A Google Cloud Project with the **Calendar API enabled**.
-   A **Service Account JSON key** downloaded from your Google Cloud Project.
-   A **Gemini API Key** from Google AI Studio.

### Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/parthCJ/calendar-agent.git](https://github.com/parthCJ/calendar-agent.git)
    cd calendar-agent
    ```

2.  **Create the environment file:**
    Create a file named `.env` in the root directory of the project. Copy the contents of `.env.example` (if available) or use the structure below and populate it with your credentials.

    ```env
    # --- Google Calendar Credentials ---
    # Paste the entire content of your service account JSON file on a single line
    GOOGLE_SERVICE_ACCOUNT_JSON='{"type": "service_account", "project_id": "...", ...}'

    # The ID of the Google Calendar to manage (e.g., your-email@gmail.com)
    GOOGLE_CALENDAR_ID="your-calendar-id@group.calendar.google.com"

    # --- LLM API Key ---
    GEMINI_API_KEY="PASTE_YOUR_GEMINI_API_KEY_HERE"
    ```

    > **Important:** Ensure the `GOOGLE_SERVICE_ACCOUNT_JSON` is a single, unbroken line.

3.  **Share your Google Calendar:**
    In your Google Calendar settings, share the calendar with your service account's email address (e.g., `...iam.gserviceaccount.com`) and give it **"Make changes to events"** permissions.

4.  **Build and run the application:**
    From the root directory, run the following command. This will build the Docker images for the frontend and backend and start the services.
    ```bash
    docker-compose up --build
    ```

5.  **Access the application:**
    Once the containers are running, open your web browser and navigate to:
    [**http://localhost:8501**](http://localhost:8501)

## 🏛️ Architecture

The application uses a modern, decoupled architecture:

-   **Streamlit Frontend:** A lightweight client that handles user interaction and communicates with the backend via HTTP requests.
-   **FastAPI Backend:** A high-performance API server that hosts the LangGraph agent, manages business logic, and securely handles all communication with external services like the Google Calendar API.

This separation of concerns makes the application modular, easier to maintain, and scalable.

## ☁️ Deployment

The application is fully containerized using Docker, allowing for consistent and reproducible deployments on any cloud platform that supports Docker containers, such as Railway, Render, or Fly.io.
