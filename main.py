import os
import pandas as pd
from flask import Flask, render_template, request, jsonify



# Initialize Flask app
app = Flask(__name__)

# Path to the updated dataset file
file_path = r"C:\Users\Sayli\Desktop\project\datasets\updated_food_pairings (1).csv"

# Function to load the CSV file into a pandas DataFrame
def load_dataset():
    if os.path.exists(file_path):
        try:
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

    return render_template('index2.html')  # Renders the input page

 #Route to handle search and show results
app.route('/results', methods=['POST'])
def results():

    ingredients = request.form.get('ingredients')  # Get user input
    df = load_dataset()

    if df is not None and ingredients:
        ingredient_list = [ingredient.strip().lower() for ingredient in ingredients.split(',')]

        # Filter dataset based on ingredient presence
        filtered_data = df[df['Ingredient'].str.lower().apply(lambda x: any(ing in x for ing in ingredient_list))]

        if not filtered_data.empty:
            filtered_data_html = filtered_data.to_html(classes='table table-bordered table-striped', index=False)
        else:
            filtered_data_html = "<p>No results found for the given ingredients.</p>"
    else:
        filtered_data_html = "<p>No results found or dataset not loaded.</p>"

    return render_template(
        'results.html',
        original_ingredients=ingredients,
        data_preview=filtered_data_html
    )

 #Start the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=5001)
