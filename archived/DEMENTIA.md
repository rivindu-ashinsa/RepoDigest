# XPredators Dementia Prediction

## Overview
This project implements a machine learning pipeline for dementia prediction using a dataset hosted on Google Drive. The pipeline includes data loading, exploration, preprocessing, feature selection, dimensionality reduction via PCA, and training/evaluation of Logistic Regression and Random Forest models, ultimately selecting Logistic Regression for better generalization.

## Key Features
- **Data Loading**: Downloads and loads a CSV dataset from Google Drive, consisting of approximately 195,000 rows and 1,024 columns with mixed data types.
- **Data Preprocessing**: Removes medical-related columns, converts data to numeric, fills missing values with medians, and applies variance thresholding to eliminate low-variance features.
- **Feature Selection**: Identifies and removes low-information columns (e.g., those with >80% single value frequency) and highly correlated features (>0.9 correlation).
- **Dimensionality Reduction**: Performs Principal Component Analysis (PCA) with 30 components after standardization to reduce dimensions while analyzing key loadings.
- **Model Training and Evaluation**: Trains Logistic Regression and Random Forest models on a 60/40 train/test split, evaluates using accuracy, precision, recall, F1-score, and confusion matrices; compares performance to select the best model.

## Tech Stack
- **Python Libraries**: 
  - `gdown` for Google Drive downloads
  - `pandas` and `numpy` for data manipulation
  - `scikit-learn` for preprocessing (VarianceThreshold, StandardScaler), PCA, LogisticRegression, RandomForestClassifier, and metrics (accuracy_score, classification_report, confusion_matrix)
  - `matplotlib` and `seaborn` for visualization (heatmaps, confusion matrices)

## Project Structure
- `.gitignore`: Configuration file specifying patterns for files to ignore in version control (e.g., *.docx, *.py, *.tmp).
- `.ipynb_checkpoints/Untitled-checkpoint.ipynb`: Automatically generated checkpoint for notebook state recovery (empty JSON structure).
- `XPredators_Demantia_Prediction.ipynb`: Main Jupyter notebook containing the complete dementia prediction pipeline, from data download to model evaluation.

## Setup Instructions
1. Ensure Python 3.x is installed on your system.
2. Install required dependencies using pip:
   ```
   pip install gdown pandas numpy scikit-learn matplotlib seaborn
   ```
3. Open the project in a Jupyter Notebook environment (recommended: Google Colab).
4. Upload `XPredators_Demantia_Prediction.ipynb` or clone the repository.
5. Ensure internet access for Google Drive downloads if running locally.

## Usage
1. Run the notebook cells sequentially starting from the first cell.
2. The notebook will:
   - Download the dataset using `gdown` with file ID `19mKGPNFb35kG__3Eihazyv5O69ZUxDcF`.
   - Perform exploratory data analysis, preprocessing, and feature selection.
   - Apply PCA for dimensionality reduction.
   - Train Logistic Regression and Random Forest models.
   - Display evaluation metrics, confusion matrices, and plots.
3. View outputs such as processed DataFrames (`X_selected`, `y`), trained models (`lr_model`, `rf_model`), and performance reports.

Key configurations include:
- VarianceThreshold: threshold=1
- Low-information removal: >80% single value frequency
- Correlation threshold: >0.9 for feature dropping
- PCA: n_components=30
- Random Forest: n_estimators=300, max_depth=None, random_state=42
- Logistic Regression: penalty='l2' (default)
- Train/test split: test_size=0.4, random_state=42

## Contributing
Contributions are welcome. Please submit pull requests with clear descriptions of changes or open issues for feature requests and bug reports.

## License
This project is licensed under the MIT License. See the LICENSE file for details.