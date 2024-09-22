import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import openai
import pandas as pd
import warnings

#Written by Sahil Pai

warnings.filterwarnings("ignore", category=FutureWarning)
# Set up your OpenAI API key
openai.api_key = 'API KEY HERE'

# Global variables to store file paths
predicted_file_path = None
actual_file_path = None


# Function to handle the file input for predicted values
def upload_predicted_file():
    global predicted_file_path
    predicted_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if predicted_file_path:
        messagebox.showinfo("File Upload", "Predicted values file uploaded successfully.")


# Function to handle the file input for actual values
def upload_actual_file():
    global actual_file_path
    actual_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if actual_file_path:
        messagebox.showinfo("File Upload", "Actual values CSV file uploaded successfully.")


# Function to handle the comparison and processing with GPT
# Function to handle the comparison and processing with GPT
def compare_and_process():
    if not predicted_file_path or not actual_file_path:
        messagebox.showerror("File Missing", "Please upload both the predicted and actual values files.")
        return

    try:
        # Read the predicted values file and show column names
        df_predicted = pd.read_csv(predicted_file_path, delim_whitespace=True)
        print("Predicted file columns:", df_predicted.columns)

        # Read the actual values CSV file and show column names
        df_actual = pd.read_csv(actual_file_path)
        print("Actual file columns:", df_actual.columns)

        # Extract the Mercury and Zinc forecast percentages from the predicted file
        mercury_predicted = df_predicted[('Forecast')].tolist()
        zinc_predicted = df_predicted[('Forecast.1')].tolist()

        # Extract the Mercury and Zinc actual percentages from the actual file
        mercury_actual = df_actual['Mercury (%)'].tolist()
        zinc_actual = df_actual['Zinc (%)'].tolist()

        # Process the comparison and send to GPT
        process_comparison_with_gpt(mercury_predicted, zinc_predicted, mercury_actual, zinc_actual)

    except KeyError as ke:
        messagebox.showerror("Column Error", f"An error occurred: {ke}. Check the column names in your files.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")



# Function to handle the GPT processing and display results
# Function to handle the GPT processing and display results
# Function to handle the GPT processing and display results
def process_comparison_with_gpt(mercury_predicted, zinc_predicted, mercury_actual, zinc_actual):
    prompt = (f"Here are the predicted and actual toxic mineral percentages for Mercury and Zinc:\n"
              f"Predicted Mercury: {mercury_predicted}\n"
              f"Actual Mercury: {mercury_actual}\n"
              f"Predicted Zinc: {zinc_predicted}\n"
              f"Actual Zinc: {zinc_actual}\n"
              "Based on this comparison, should the mining company continue mining in this location? "
              "Please provide a short sentence like 'Yes, you should continue mining' or 'No, you shouldn't continue mining'.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an AI assistant that advises on mining decisions based on a comparison of predicted and actual toxic mineral values."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the response from GPT
        bot_response = response['choices'][0]['message']['content'].strip()

        # Display the result in a pop-up window
        messagebox.showinfo("Mining Decision", bot_response)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while communicating with GPT: {str(e)}")


# Function to clear all text in both text areas
def clear_text():
    user_input_text.delete("1.0", tk.END)
    bot_reply_text.config(state=tk.NORMAL)
    bot_reply_text.delete("1.0", tk.END)
    bot_reply_text.insert(tk.END, "Bot: Text cleared.\n")
    bot_reply_text.config(state=tk.DISABLED)


# Create the main window
root = tk.Tk()
root.title("Mining Decision Bot")

# Create and configure the user input text area
user_input_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
user_input_text.pack(pady=10)

# Create and configure the bot reply text area
bot_reply_text = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
bot_reply_text.pack(pady=10)
bot_reply_text.insert(tk.END, "Bot: Welcome! Please upload your data files.\n")
bot_reply_text.config(state=tk.DISABLED)

# Create buttons for file uploads
upload_predicted_button = tk.Button(root, text="Upload Predicted Values File", command=upload_predicted_file)
upload_predicted_button.pack(pady=10)

upload_actual_button = tk.Button(root, text="Upload Actual Values CSV", command=upload_actual_file)
upload_actual_button.pack(pady=10)

# Create button to compare and process the data
compare_button = tk.Button(root, text="Compare and Process", command=compare_and_process)
compare_button.pack(pady=10)

# Create and configure the clear button
clear_button = tk.Button(root, text="Clear All", command=clear_text)
clear_button.pack(pady=10)

root.mainloop()
