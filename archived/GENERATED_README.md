# MetaMorphs: Lung Cancer Prediction System

## Project Overview

MetaMorphs is a comprehensive machine learning system designed for predicting lung cancer survival status. The project implements a complete data science pipeline that processes raw medical data through advanced preprocessing techniques and trains multiple machine learning models to achieve high-accuracy predictions.

The system includes a trained neural network model and a reusable data preprocessing pipeline, achieving approximately 82% accuracy with Random Forest and 83% precision on the validation set.

## Key Features

- **Complete Data Pipeline**: Custom scikit-learn pipeline with specialized transformers for medical data processing
- **Multiple ML Models**: Implementation and comparison of Logistic Regression, Random Forest, K-Nearest Neighbors, and Neural Network models
- **Advanced Preprocessing**: Handles smoking status processing, date formatting, categorical encoding, and feature scaling
- **Trained Neural Network**: Ready-to-use Keras/TensorFlow model for binary classification
- **Model Performance Tracking**: Comprehensive evaluation framework with accuracy, precision, recall, and AUC metrics
- **Reusable Components**: Encapsulated preprocessing pipeline for consistent data transformation

## Tech Stack

- **Python 3.11+**
- **Deep Learning**: TensorFlow/Keras for neural network implementation
- **Machine Learning**: scikit-learn for traditional ML models and preprocessing
- **Data Manipulation**: pandas, numpy
- **Visualization**: matplotlib
- **Model Persistence**: joblib for pipeline serialization, Keras SavedModel format
- **Development Environment**: Jupyter Notebook

## Project Structure

```
├── ExportedModel/
│   └── MetaMorphs_model.h5          # Trained Keras/TensorFlow model
├── data_pipeline.pkl                # Serialized preprocessing pipeline
├── metamorphs (1).ipynb             # Main Jupyter notebook with complete workflow
├── .gitignore                       # Git ignore configuration
└── README.md                        # Project documentation
```

## Setup Instructions

### Prerequisites

1. Install Python 3.11 or higher
2. Install required dependencies:

```bash
pip install tensorflow keras scikit-learn pandas numpy matplotlib joblib
```

### Repository Setup

1. Clone or download the repository files
2. Ensure the following files are present:
   - `ExportedModel/MetaMorphs_model.h5` (trained model)
   - `data_pipeline.pkl` (preprocessing pipeline)
   - `metamorphs (1).ipynb` (main notebook)

### Data Requirements

- Training and test datasets from Kaggle competition: `/kaggle/input/idealize-2025-datathon-competition/`
- Expected data columns: `sex`, `patient_age`, `height_cm`, `weight_kg`, `cigarettes_per_day`, `cholesterol_mg_dl`, `family_cancer_history`, `smoking_status`, `treatment_type`

## Usage

### Using the Trained Model

```python
import tensorflow as tf
import numpy as np

# Load the trained model
model = tf.keras.models.load_model('ExportedModel/MetaMorphs_model.h5')

# Prepare input data (22-dimensional float32 array)
input_data = np.array([[...]], dtype=np.float32)  # Your 22-D features

# Make predictions
predictions = model.predict(input_data)
# Output: scalar probability in [0, 1] for binary classification
```

### Using the Data Pipeline

```python
import joblib

# Load the preprocessing pipeline
pipeline = joblib.load('data_pipeline.pkl')

# For training
pipeline.fit(training_data)

# For inference on new data
processed_data = pipeline.transform(new_data)

# Use processed data with any ML model
predictions = model.predict(processed_data)
```

### Running the Complete Workflow

1. Open `metamorphs (1).ipynb` in Jupyter Notebook
2. Run cells sequentially to:
   - Load and explore the data
   - Apply preprocessing transformations
   - Train and evaluate multiple models
   - Compare performance metrics
   - Generate predictions

## Preprocessing Pipeline Components

The data pipeline includes these specialized transformers:

- **ProcessSmoking**: Custom transformer for smoking-related data processing
- **ProcessCols**: Column data processing and feature engineering
- **FormatDates**: Date field formatting and datetime processing
- **OneHotEncoder**: Categorical encoding for `smoking_status` and `treatment_type`
- **DropUnwantedCols**: Removes irrelevant columns
- **StandardScaler**: Feature scaling (mean=0, variance=1)

## Model Performance

The system was evaluated on multiple models:

- **Best Performer**: Random Forest
  - Accuracy: ~82%
  - Precision: ~83%
- **Neural Network**: Sequential MLP with 128→64→32 hidden layers
  - Uses ReLU activation and 30% dropout regularization
  - Optimized with Adam (lr=0.001) and binary crossentropy loss
  - Tracked metrics: accuracy, precision, recall, AUC

## Architecture Details

### Neural Network Model
- **Input**: 22-dimensional feature vector (float32)
- **Hidden Layers**: 
  - Dense(128, ReLU) + Dropout(0.3)
  - Dense(64, ReLU) + Dropout(0.3)
  - Dense(32, ReLU)
- **Output**: Single sigmoid unit for binary classification

### Data Preprocessing
- **Categorical Encoding**: One-hot encoding for smoking status (Current/Former/Never/Passive) and treatment type (Chemotherapy/Combined/Radiation/Surgery)
- **Feature Scaling**: StandardScaler for normalized features
- **Data Cleaning**: Handles missing values and removes irrelevant columns

## Contributing

This project was developed as part of a data science competition. For improvements:

1. Fork the repository
2. Create a feature branch
3. Implement changes with appropriate documentation
4. Submit a pull request with detailed description

## License

This project was developed for educational and research purposes as part of the Idealize 2025 Datathon Competition.

---

*For questions or support, please refer to the main Jupyter notebook `metamorphs (1).ipynb` which contains detailed implementation notes and explanations.*