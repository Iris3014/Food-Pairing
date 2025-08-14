import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Path to the Food and Beverages Pairing dataset
file_path = r"C:\Users\Sayli\Desktop\project\datasets\final_FoodWinePairing.csv"

# Function to load dataset
def load_dataset():
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()
            print("Dataset loaded successfully!")
            return df
        except Exception as e:
            print(f"Error reading the file: {e}")
            return None
    else:
        print(f"File not found at {file_path}")
        return None

@app.route('/')
def index():
    return render_template('food_wine.html')

@app.route('/results', methods=['POST'])
def results():
    food_query = request.form.get('food_query')
    df = load_dataset()

    if df is not None and food_query:
        filtered_data = df[df['Food'].str.contains(food_query, case=False, na=False)]
        filtered_data_html = filtered_data.to_html(classes='table table-bordered table-striped', index=False)
    else:
        filtered_data_html = "No results found or dataset not loaded."

    return render_template(
        'food_wine_result.html',
        food_query=food_query,
        data_preview=filtered_data_html
    )

if __name__ == '__main__':
    app.run(debug=True, port=9000)
