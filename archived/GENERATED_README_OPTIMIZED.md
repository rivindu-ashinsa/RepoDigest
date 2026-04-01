# MetaMorphs - Lung Cancer Prediction Model

A machine learning project for predicting lung cancer outcomes using medical and demographic data, developed for the Idealize 2025 Datathon competition.

## Project Overview

This repository contains a complete machine learning pipeline for binary classification of lung cancer cases. The project implements a deep neural network trained on medical data including smoking status, treatment types, demographics, and various clinical features to predict lung cancer survival outcomes.

## Key Features

- **Complete ML Pipeline**: End-to-end solution from raw data to final predictions
- **Robust Data Preprocessing**: Custom scikit-learn pipeline handling:
  - Smoking status preprocessing with custom transformers
  - Treatment type encoding and categorization
  - Date formatting and temporal feature extraction
  - Categorical variable encoding using OneHotEncoder
  - Feature standardization with StandardScaler
- **Deep Learning Model**: Sequential neural network with:
  - 4 Dense layers with ReLU activation
  - Dropout layers for regularization (30% rate)
  - Sigmoid output for binary classification
  - Binary crossentropy loss with Adam optimizer
- **Model Performance Tracking**: Multi-metric evaluation including accuracy, precision, recall, and AUC
- **Export-Ready Artifacts**: Serialized model and preprocessing pipeline for easy deployment

## Tech Stack

### Core Technologies
- **Python 3.11+**
- **TensorFlow/Keras** - Deep learning framework
- **Scikit-learn** - Machine learning pipeline and preprocessing
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing

### Key Libraries
- `h5py` - HDF5 file format support for model serialization
- `joblib` - Pipeline serialization and deserialization
- `matplotlib` - Visualization capabilities

## Project Structure

```
├── .gitignore                          # Git configuration for ignored files
├── ExportedModel/
│   ├── MetaMorphs_model.h5            # Trained Keras model (architecture + weights)
│   └── data_pipeline.pkl              # Serialized preprocessing pipeline
├── metamorphs (1).ipynb               # Main Jupyter notebook with complete implementation
└── README.md                          # Project documentation (this file)
```

### File Descriptions

- **`.gitignore`**: Specifies CSV files (test.csv, train.csv, submission.csv) to be excluded from version control
- **`MetaMorphs_model.h5`**: Keras SavedModel containing:
  - Neural network architecture (4 Dense layers + Dropout)
  - Trained weights and optimizer state
  - Model configuration and training metadata
- **`data_pipeline.pkl`**: Scikit-learn Pipeline object with preprocessing steps:
  - `ProcessSmoking`: Custom smoking status preprocessing
  - `ProcessCols`: Custom column processing
  - `FormatDates`: Date formatting transformations
  - `EncodeCatCols`: OneHot encoding for categorical variables
  - `DropUnwantedCols`: Feature selection step
  - `StandardScaler`: Feature normalization
- **`metamorphs (1).ipynb`**: Main execution notebook containing complete ML workflow

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Kaggle account (for competition data access)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd metamorphs-lung-cancer-prediction
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install tensorflow scikit-learn pandas numpy matplotlib h5py joblib
   ```

4. **Data Setup**
   - Download competition data from Kaggle
   - Place `train.csv` and `test.csv` in the appropriate input directory
   - Ensure data paths match: `/kaggle/input/idealize-2025-datathon-competition/`

### Configuration
- **Input Shape**: 22 features (float32 array)
- **Output**: Binary classification (sigmoid probability)
- **Preprocessing**: Automatic pipeline handles all data transformations
- **Model Loading**: Use `tf.keras.models.load_model()` for complete model or separate architecture/weights loading

## Usage

### Running the Complete Pipeline

1. **Execute the main notebook**
   ```bash
   jupyter notebook "metamorphs (1).ipynb"
   ```

2. **Follow the sequential workflow**:
   - Data loading and exploration
   - Preprocessing pipeline application
   - Model training and evaluation
   - Prediction generation

### Using Pre-trained Model

```python
import tensorflow as tf
import joblib
import pandas as pd

# Load preprocessing pipeline
pipeline = joblib.load('ExportedModel/data_pipeline.pkl')

# Load trained model
model = tf.keras.models.load_model('ExportedModel/MetaMorphs_model.h5')

# For new predictions:
# raw_data = pd.read_csv('your_new_data.csv')
# processed_data = pipeline.transform(raw_data)
# predictions = model.predict(processed_data)
```

### Model Performance

The model has been evaluated across multiple algorithms with the following approximate performance:

| Algorithm | Accuracy | Precision |
|-----------|----------|-----------|
| Logistic Regression | ~78% | Variable |
| Random Forest | ~82% | High |
| K-Nearest Neighbors | ~75% | Variable |
| Neural Network | ~80% | High |

## Contributing

This project was developed for a Datathon competition. For contributions:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow the existing code structure and naming conventions
- Document any new features or modifications
- Ensure all new code includes appropriate error handling
- Test thoroughly before submitting pull requests

## License

This project was developed for educational and competition purposes. Please check with the competition organizers regarding usage rights and licensing terms for the dataset and model artifacts.

## Acknowledgments

- Idealize 2025 Datathon competition organizers
- Kaggle platform for hosting the dataset
- TensorFlow and scikit-learn communities for excellent documentation and tools

## Contact

For questions or support regarding this project, please refer to the competition documentation or create an issue in the repository.

---

**Note**: This model processes medical data and should be used for educational/research purposes only. Clinical decisions should not be based solely on machine learning predictions without proper medical validation.
```

