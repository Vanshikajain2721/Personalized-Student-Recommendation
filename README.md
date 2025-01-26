# Personalized Student Recommendation

## Project Overview
The **Personalized Student Recommendation** system aims to provide insights into a student's performance based on quiz data. By analyzing past quiz results, difficulty levels, and topics, it generates personalized recommendations that help students identify weak areas and improve their learning outcomes. 

## Features
- **Performance Analysis**: Analyzes student performance in quizzes.
- **Topic and Difficulty-Level Insights**: Provides insights into topics and difficulty levels where students need improvement.
- **Personalized Recommendations**: Suggests actions to improve performance in specific areas based on quiz data.
- **Visualizations**: Graphical representations of the student's performance and weak areas.

## Folder Structure
```
Personalized-Student-Recommendation/
├── backend/                 # Backend-related code
│   ├── app.py               # Main application file
│   └── requirements.txt     # Dependencies
├── mobile/                  # Mobile app (Flutter)
│   ├── lib/                 # Dart files for Flutter app
│   └── pubspec.yaml         # Flutter configuration
├── analysis/                # Data analysis scripts
│   ├── data_analysis.py     # Python script for data analysis
│   ├── analysis_results/    # Results folder (CSV, JSON)
│   ├── visualizations/      # Graphs (PNG, SVG)
│       └── score_distribution.png
└── README.md                # This file
```

## Getting Started

To run the project, follow these steps:

### 1. Clone the repository:
```bash
git clone https://github.com/Vanshikajain2721/Personalized-Student-Recommendation.git
```

### 2. Install Backend Dependencies:
For the backend part, navigate to the `backend/` directory and install the required dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### 3. Data Analysis:
For running the data analysis, navigate to the `analysis/` directory and run the Python script:
```bash
cd analysis
python data_analysis_api.py
```

This will generate insights about quiz performance, weak areas, and provide recommendations.

### 4. Run Mobile Application:
For the mobile app (built with Flutter), make sure you have Flutter installed. Then, navigate to the `mobile/` directory and run:
```bash
cd mobile
flutter run
```

This will launch the mobile application for personalized recommendations.

## Data Sources
- **Current Quiz Data**: Provides the latest quiz information and scores.
- **Historical Data**: Contains the past performance data of students for comparison.
- **Submission Data**: Contains the quiz submission results and individual answers.

## Contributing
If you'd like to contribute to the project, feel free to fork the repository, make your changes, and submit a pull request. We welcome new features, improvements, and bug fixes!
