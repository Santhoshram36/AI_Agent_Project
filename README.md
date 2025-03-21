# AI Agent Project

## Overview
This project is an AI-powered agent designed to perform automated tasks. The system consists of a backend built with FastAPI and a frontend to interact with the AI agent.

## Backend Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/Santhoshram36/AI_Agent_Project.git
   cd AI_Agent_Project
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root.
   - Add your API key inside the `.env` file:
     ```
     API_KEY=your_api_key_here
     ```

5. Start the backend server:
   ```sh
   uvicorn main:app --reload
   ```
   The server will run at `http://127.0.0.1:8000`.

## Frontend Setup

1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```

2. Install dependencies:
   ```sh
   npm install  # or yarn install
   ```

3. Start the frontend:
   ```sh
   npm start  # or yarn start
   ```
   The frontend will be available at `http://localhost:3000`.

## Usage
- Ensure the backend is running before starting the frontend.
- Open `http://localhost:3000` in your browser to access the AI Agent.

---
**Note:** Make sure to replace `your_api_key_here` with your actual API key before running the project.

