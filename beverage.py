import os
import pandas as pd
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Path to the Food and Beverages Pairing dataset located in the 'datasets' folder
file_path = r"C:\Users\Sayli\Desktop\project\datasets\doubled_FoodBeveragePairing.csv"

# Function to load the CSV file into a pandas DataFrame
def load_dataset():
    if os.path.exists(file_path):
        try:
            # Load the dataset into a pandas DataFrame
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()  # Strip any leading/trailing spaces
            print("Dataset loaded successfully!")
            return df
        except Exception as e:
            print(f"Error reading the file: {e}")
            return None
    else:
        print(f"File not found at {file_path}. Please check the file path.")
        return None

# Route to the input page
@app.route('/')
def index():
    return render_template('beverage.html')  # Render the input page

# Route to handle the search and show results on a new page
@app.route('/results', methods=['POST'])
def results():
    food_query = request.form.get('food_query')  # Get the food item from the form input
    df = load_dataset()

    if df is not None and food_query:
        # Filter the dataset based on the food item
        filtered_data = df[df['Food'].str.contains(food_query, case=False, na=False)]

        # Convert filtered data to HTML table format
        filtered_data_html = filtered_data.to_html(classes='table table-bordered table-striped', index=False)
    else:
        filtered_data_html = "No results found or dataset not loaded."

    return render_template(
        'beverageresult.html',
        food_query=food_query,
        data_preview=filtered_data_html
    )

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=8080)
