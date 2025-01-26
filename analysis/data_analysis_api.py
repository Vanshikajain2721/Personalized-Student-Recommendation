from flask import Flask, jsonify, send_file
import pandas as pd
import requests
import matplotlib.pyplot as plt
from waitress import serve

app = Flask(__name__)

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Function to fetch data from the provided APIs
def fetch_data(api_url):
    try:
        response = requests.get(api_url, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {api_url}: {e}")
        return None

# Load data from APIs
def load_data():
    current_data_url = "https://www.jsonkeeper.com/b/LLQT"
    sub_data_url = "https://api.jsonserve.com/rJvd7g"
    historical_data_url = "https://api.jsonserve.com/XgAgFJ"

    current_data = fetch_data(current_data_url)
    sub_data = fetch_data(sub_data_url)
    historical_data = fetch_data(historical_data_url)

    if not all([current_data, sub_data, historical_data]):
        return None, None, None  # Handle failure gracefully

    return (
        pd.json_normalize(current_data),
        pd.json_normalize(sub_data),
        pd.json_normalize(historical_data),
    )

Current_df, Sub_data_df, Historical_df = load_data()

if any(df.empty for df in [Current_df, Sub_data_df, Historical_df]):
    print("Error: One or more data sources could not be loaded.")
    # Handle gracefully

# Generate visualizations
def generate_visualizations(sub_data_df, historical_df):
    try:
        plt.figure(figsize=(10, 5))
        plt.hist(historical_df["score"], bins=10, alpha=0.7, label="Historical Scores")
        plt.axvline(sub_data_df["score"].mean(), color="red", linestyle="dashed", linewidth=1, label="Current Avg. Score")
        plt.title("Score Distribution")
        plt.xlabel("Score")
        plt.ylabel("Frequency")
        plt.legend()
        # Use a path that ensures the file is saved correctly on Render
        plt.savefig("/tmp/score_distribution.png")
    except Exception as e:
        print(f"Error during visualization: {e}")

# Load and preprocess data
Current_df, Sub_data_df, Historical_df = load_data()

# Example analysis (basic stats, comparison)
average_score = Sub_data_df["score"].mean()
average_accuracy = Sub_data_df["accuracy"].str.replace("%", "").astype(float).mean()
historical_avg_score = Historical_df["score"].mean()
current_avg_score = Current_df["quiz.correct_answer_marks"].astype(float).mean()

@app.route('/insights', methods=['GET'])
def get_insights():
    insights = {
        "average_score": average_score,
        "average_accuracy": f"{average_accuracy:.2f}%",
    }
    return jsonify(insights)

@app.route('/comparison', methods=['GET'])
def get_comparison():
    comparison = {
        "current_avg_score": current_avg_score,
        "historical_avg_score": historical_avg_score,
    }
    return jsonify(comparison)

@app.route('/visualization', methods=['GET'])
def get_visualization():
    generate_visualizations(Sub_data_df, Historical_df)
    return send_file("score_distribution.png", mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)



if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
