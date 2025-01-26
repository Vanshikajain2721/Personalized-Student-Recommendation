import pandas as pd
import requests
import matplotlib.pyplot as plt

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Function to fetch data from the provided APIs
def fetch_data(api_url):
    try:
        response = requests.get(api_url, verify=False)  # Disable SSL verification
        response.raise_for_status()  # Check if the request was successful
        return response.json()  # Parse the JSON response
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
        print("Error: One or more data sources could not be loaded. Exiting.")
        exit()

    return (
        pd.json_normalize(current_data),
        pd.json_normalize(sub_data),
        pd.json_normalize(historical_data),
    )

# Merge current quiz data into the submission data
def merge_current_to_submission(sub_data_df, current_df):
    try:
        merged_df = sub_data_df.merge(
            current_df,
            left_on="quiz_id",
            right_on="quiz.id",
            suffixes=("_sub", "_current"),
            how="left",
        )
        if "quiz.topic" in merged_df.columns:
            merged_df["topic"] = merged_df["quiz.topic"]
        else:
            print("Warning: 'quiz.topic' column missing in merged data. Adding 'Unknown'.")
            merged_df["topic"] = "Unknown"

        merged_df["topic"].fillna("Unknown", inplace=True)
        return merged_df
    except Exception as e:
        print(f"Error during merging: {e}")
        exit()

# Analyze basic performance stats
def analyze_basic_stats(sub_data_df):
    try:
        average_score = sub_data_df["score"].mean()
        sub_data_df["accuracy_numeric"] = sub_data_df["accuracy"].str.replace("%", "").astype(float)
        average_accuracy = sub_data_df["accuracy_numeric"].mean()

        print("\nBasic Performance Stats:")
        print(f"Average Score: {average_score}")
        print(f"Average Accuracy: {average_accuracy}%")
    except Exception as e:
        print(f"Error during basic stats analysis: {e}")

# Compare current quiz with historical data
def compare_with_historical(current_df, historical_df):
    try:
        historical_avg_score = historical_df["score"].mean()
        current_avg_score = current_df["quiz.correct_answer_marks"].astype(float).mean()

        print("\nComparing Current Quiz to Historical Data:")
        print(f"Current Quiz Score: {current_avg_score}")
        print(f"Average Historical Score: {historical_avg_score}")
    except Exception as e:
        print(f"Error during comparison: {e}")

# Generate visualizations
def generate_visualizations(sub_data_df, historical_df):
    try:
        # Bar graph for score distribution
        historical_scores = historical_df["score"]
        plt.figure(figsize=(10, 5))
        plt.hist(historical_scores, bins=10, alpha=0.7, label="Historical Scores")
        plt.axvline(sub_data_df["score"].mean(), color="red", linestyle="dashed", linewidth=1, label="Current Avg. Score")
        plt.title("Score Distribution")
        plt.xlabel("Score")
        plt.ylabel("Frequency")
        plt.legend()
        plt.savefig("analysis/visualizations/score_distribution.png")
        plt.show()
    except Exception as e:
        print(f"Error during visualization: {e}")

# Main function
def main():
    try:
        Current_df, Sub_data_df, Historical_df = load_data()

        print("\nCurrent Quiz Data Info:")
        print(Current_df.info())
        print("\nSubmission Data Info:")
        print(Sub_data_df.info())
        print("\nHistorical Data Info:")
        print(Historical_df.info())

        # Merge DataFrames
        Sub_data_df = merge_current_to_submission(Sub_data_df, Current_df)

        # Analyze basic stats
        analyze_basic_stats(Sub_data_df)

        # Compare with historical data
        compare_with_historical(Current_df, Historical_df)

        # Generate visualizations
        generate_visualizations(Sub_data_df, Historical_df)
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
