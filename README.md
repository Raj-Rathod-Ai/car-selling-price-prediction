# Car Value Estimator - Streamlit App

This is a premium, conversational Streamlit application designed for estimating selling price value of pre-owned cars.

## Features & Questionnaire Flow
The application guides the user through a simple 9-step conversational questionnaire:
1. **Car Model**: Choose model from a dropdown list of 98 models.
2. **Manufacturing Year**: Enter the year of manufacturer.
3. **Showroom Price**: Estimate present showroom price (Lakhs). Can use default of 6.4 Lakhs if unknown.
4. **Kilometers Driven**: Enter odometer reading.
5. **Fuel Type**: Pick fuel type (CNG, Diesel, Petrol).
6. **Seller Type**: Sell as an Individual or through a Dealer.
7. **Transmission Type**: Select Manual or Automatic.
8. **Previous Owners**: Number of previous owners (0 to 3).
9. **Prediction**: Summarize answers and calculate estimated selling price (in Lakhs).

## How to Run Locally

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Deploying to Streamlit Community Cloud

1. Push this directory to your GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and connect your repository.
3. Set the main file path to `app.py`.

## Keep-Alive Configuration (No-Sleep Workflow)
Streamlit Community Cloud automatically puts applications to sleep after 7 days of inactivity. 

To keep this application awake continuously:
1. Go to your GitHub repository -> **Settings** -> **Secrets and variables** -> **Actions**.
2. Click **New repository secret**.
3. Name the secret **`APP_URL`**.
4. Set the value to the deployed URL of your Streamlit app (e.g., `https://your-app-name.streamlit.app`).
5. The daily GitHub Action in `.github/workflows/keep_alive.yml` will automatically ping this URL to ensure it never goes to sleep.
