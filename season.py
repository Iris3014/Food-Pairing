from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load dataset
file_path = r"C:\Users\Sayli\Desktop\project\datasets\season.csv"

try:
    df = pd.read_csv(file_path)
    print(df.head())  # Debugging: Print first 5 rows to check if CSV is loaded
except Exception as e:
    print("Error loading CSV:", e)

@app.route('/')
def home():

    return render_template("season.html")  # Render the frontend

@app.route('/pairings', methods=['GET'])
def get_pairings():

    data = df.to_dict(orient='records')
    return jsonify(data)

@app.route('/pairings/season/<season>', methods=['GET'])
def get_pairings_by_season(season):

    filtered_data = df[df['Season'].str.lower() == season.lower()].to_dict(orient='records')
    return jsonify(filtered_data)

@app.route('/pairings/cuisine/<cuisine>', methods=['GET'])
def get_pairings_by_cuisine(cuisine):

    filtered_data = df[df['Cuisine'].str.lower() == cuisine.lower()].to_dict(orient='records')
    return jsonify(filtered_data)

@app.route('/pairings/ingredient/<ingredient>', methods=['GET'])
def get_pairings_by_ingredient(ingredient):

    filtered_data = df[df['Ingredient'].str.lower() == ingredient.lower()].to_dict(orient='records')
    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(debug=True,port=5003 )
