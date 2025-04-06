# Project Title

Investimate - Personalized Investment Recommendations

## Description

Investimate is a financial assistant that provides personalized investment recommendations based on the user's risk profile. It leverages machine learning models to analyze user data and generate tailored investment suggestions.

## Features

- **Risk Score Calculation**: Calculates the user's risk score based on their profile.
- **Personalized Recommendations**: Provides investment recommendations aligned with the user's risk appetite.
- **Chatbot Integration**: Allows users to interact with a chatbot for personalized financial advice.
- **Volatility Calculation**: Computes the rolling standard deviation of asset returns to measure volatility.

## Technologies Used

- **Python**: Backend logic and data processing.
- **JavaScript**: Frontend interactivity.
- **Pandas**: Data manipulation and analysis.
- **Google Generative AI**: For generating responses and recommendations.
- **Django**: Web framework for building the application.
- **HTML/CSS**: Frontend structure and styling.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/PratikshaAigal/investimate.git
    cd investimate
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the project root.
    - Add your Gemini API key:
      ```
      GEMINI_API_KEY=your_api_key_here
      ```

5. **Run the Django server**:
    ```bash
    python manage.py runserver
    ```

## Usage

1. **Access the application**:
    Open your web browser and navigate to `http://127.0.0.1:8000`.

2. **Interact with the chatbot**:
    Use the chatbot interface to ask questions and get personalized investment advice.

3. **View your risk score and recommendations**:
    The application will display your risk score and tailored investment recommendations based on your profile.

## File Structure

- `api/`: Contains the backend logic and API endpoints.
  - `utils/gemini.py`: Handles communication with the Gemini API.
- `templates/`: Contains HTML templates for rendering the frontend.
  - `risk_score.html`: Displays the user's risk score and recommendations.
- `static/`: Contains static files like CSS and JavaScript.
- `manage.py`: Django's command-line utility for administrative tasks.

