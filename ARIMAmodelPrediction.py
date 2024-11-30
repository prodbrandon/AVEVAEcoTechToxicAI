import pandas as pd
from io import StringIO
import os
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, r2_score
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import warnings
from statsmodels.tools.sm_exceptions import ValueWarning

#Written by Sahil Pai, Brandon Lim

# Suppress specific warnings related to statsmodels date index and future warnings
warnings.filterwarnings("ignore", category=ValueWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

register_matplotlib_converters()

# Function to allow file selection from the computer
def select_file():
    Tk().withdraw()  # Prevent Tkinter window from showing up
    file_path = askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])
    return file_path

# Prompt user to select the file
file_path = select_file()

# Load the selected file into a pandas DataFrame
df = pd.read_csv(file_path)

# Define the cleaning and preprocessing function
def clean_and_preprocess(df):
    """
    Clean and preprocess the data for ARIMA modeling.

    Parameters:
    df (pandas.DataFrame): The original dataframe containing the raw data.

    Returns:
    pandas.DataFrame: Cleaned and preprocessed dataframe.
    """
    # Step 1: Drop any unnecessary columns
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # Step 2: Handle missing values (if any)
    df = df.dropna()  # Drop rows with missing values (you can use fillna if you want to impute them)

    # Step 3: Convert 'Date' column to datetime if it's not already
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])  # Drop rows where date conversion failed

    # Step 4: Set 'Date' as the index for time series analysis
    df.set_index('Date', inplace=True)

    # Step 5: Ensure all numeric columns are of the correct data type
    numeric_columns = ['Mercury (%)', 'Lead (%)', 'Zinc (%)', 'Copper (%)', 'Dirt Amount (kg)']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Step 6: Handle any remaining missing or invalid data after conversion
    df = df.dropna()

    return df

# Clean and preprocess the data
df = clean_and_preprocess(df)

# Visualize the cleaned time series data
plt.figure(figsize=(10, 6))
plt.plot(df['Mercury (%)'], label='Mercury (%)')
plt.plot(df['Zinc (%)'], label='Zinc (%)')
plt.title('Mercury and Zinc Levels Over Time')
plt.legend()
plt.show()

# Define a function to fit an ARIMA model and make predictions
def fit_arima(series, order):
    model = ARIMA(series, order=order)
    model_fit = model.fit()
    return model_fit

# Define the ARIMA order (p, d, q)
arima_order = (10, 1, 0)

# Fit ARIMA for Mercury levels
mercury_model = fit_arima(df['Mercury (%)'], arima_order)

# Fit ARIMA for Zinc levels
zinc_model = fit_arima(df['Zinc (%)'], arima_order)

# Print summary of the models
print(mercury_model.summary())
print(zinc_model.summary())

# Make predictions for the next 10 days
future_dates = pd.date_range(start='2024-01-01', periods=10, freq='D')

# Forecast future Mercury and Zinc levels
mercury_forecast = mercury_model.forecast(steps=10)
zinc_forecast = zinc_model.forecast(steps=10)

# Create a DataFrame for future predictions
forecast_df = pd.DataFrame({
    'Date': future_dates,
    'Mercury Forecast (%)': mercury_forecast,
    'Zinc Forecast (%)': zinc_forecast
})

# Set 'Date' as the index
forecast_df.set_index('Date', inplace=True)

# Visualize the forecasted values
plt.figure(figsize=(10, 6))
plt.plot(df.index[-50:], df['Mercury (%)'].tail(50), label='Observed Mercury')
plt.plot(forecast_df.index, forecast_df['Mercury Forecast (%)'], label='Forecasted Mercury', linestyle='--')
plt.title('Mercury Levels Forecast')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(df.index[-50:], df['Zinc (%)'].tail(50), label='Observed Zinc')
plt.plot(forecast_df.index, forecast_df['Zinc Forecast (%)'], label='Forecasted Zinc', linestyle='--')
plt.title('Zinc Levels Forecast')
plt.legend()
plt.show()

# Evaluate the model by calculating the mean squared error and R² on the training data
mercury_mse = mean_squared_error(df['Mercury (%)'], mercury_model.fittedvalues)
zinc_mse = mean_squared_error(df['Zinc (%)'], zinc_model.fittedvalues)

# Calculate the R² score (percentage accuracy)
mercury_r2 = r2_score(df['Mercury (%)'], mercury_model.fittedvalues)
zinc_r2 = r2_score(df['Zinc (%)'], zinc_model.fittedvalues)

mercury_accuracy = mercury_r2 * 100  # Convert R² score to percentage
zinc_accuracy = zinc_r2 * 100  # Convert R² score to percentage

# Print the MSE and Accuracy
# print(f'Mercury Model MSE: {mercury_mse}, Mercury Model Accuracy: {mercury_accuracy:.2f}%')
# print(f'Zinc Model MSE: {zinc_mse}, Zinc Model Accuracy: {zinc_accuracy:.2f}%')

# Display the future forecast
print(forecast_df)

# Write the forecast to a text file in the same directory as the script
script_directory = os.path.dirname(os.path.abspath(__file__))
output_file_path = os.path.join(script_directory, 'predictedValues.txt')

# Save the forecast DataFrame to the text file
with open(output_file_path, 'w') as f:
    f.write(forecast_df.to_string())

print(f'Predicted values have been saved to {output_file_path}')
