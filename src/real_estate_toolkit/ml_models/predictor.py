from typing import List, Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error
)
import polars as pl
import pandas as pd


class HousePricePredictor:
    def __init__(self, train_data_path: str, test_data_path: str):
        """
        Initialize the predictor with paths to the training and testing datasets.

        Args:
            train_data_path (str): Path to the training dataset CSV file.
            test_data_path (str): Path to the testing dataset CSV file.
        """
        self.train_data = pl.read_csv(train_data_path)
        self.test_data = pl.read_csv(test_data_path)
        self.models = {}  # To store trained models

    def clean_data(self):
        """
        Perform data cleaning on training and testing datasets.
        """
        # Drop columns with too many missing values
        self.train_data = self.train_data.drop(["Alley", "PoolQC", "Fence", "MiscFeature"])

        # Fill missing values for both datasets
        self.train_data = self.train_data.fill_null({
            "LotFrontage": self.train_data["LotFrontage"].mean(),
            "GarageYrBlt": self.train_data["GarageYrBlt"].median(),
        })
        self.test_data = self.test_data.fill_null({
            "LotFrontage": self.test_data["LotFrontage"].mean(),
            "GarageYrBlt": self.test_data["GarageYrBlt"].median(),
        })

    def prepare_features(self, target_column: str = 'SalePrice', selected_predictors: List[str] = None):
        """
        Prepare the dataset for machine learning by separating features and target.
        """
        train_df = self.train_data.to_pandas()  # Convert to Pandas for compatibility
        test_df = self.test_data.to_pandas()

        # Separate target and predictors
        y = train_df[target_column]
        X = train_df.drop(columns=[target_column])
        X_test = test_df

        # Select specific predictors if provided
        if selected_predictors:
            X = X[selected_predictors]
            X_test = X_test[selected_predictors]

        # Identify numeric and categorical columns
        numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
        categorical_features = X.select_dtypes(include=["object", "category"]).columns

        # Create preprocessing pipelines
        numeric_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="mean")),
            ("scaler", StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ])

        # Combine pipelines
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features)
            ]
        )

        # Split data into training and testing sets
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_val, y_train, y_val, X_test, preprocessor

    def train_baseline_models(self) -> Dict[str, Dict[str, float]]:
        """
        Train and evaluate baseline models.
        """
        X_train, X_val, y_train, y_val, _, preprocessor = self.prepare_features()

        # Define models
        models = {
            "Linear Regression": Pipeline(steps=[("preprocessor", preprocessor), ("model", LinearRegression())]),
            "Random Forest": Pipeline(steps=[("preprocessor", preprocessor), ("model", RandomForestRegressor())])
        }

        results = {}

        for model_name, pipeline in models.items():
            # Train the model
            pipeline.fit(X_train, y_train)
            self.models[model_name] = pipeline

            # Evaluate the model
            y_pred_train = pipeline.predict(X_train)
            y_pred_val = pipeline.predict(X_val)

            results[model_name] = {
                "metrics": {
                    "Train MSE": mean_squared_error(y_train, y_pred_train),
                    "Validation MSE": mean_squared_error(y_val, y_pred_val),
                    "Train R2": r2_score(y_train, y_pred_train),
                    "Validation R2": r2_score(y_val, y_pred_val),
                    "Train MAE": mean_absolute_error(y_train, y_pred_train),
                    "Validation MAE": mean_absolute_error(y_val, y_pred_val),
                    "Train MAPE": mean_absolute_percentage_error(y_train, y_pred_train),
                    "Validation MAPE": mean_absolute_percentage_error(y_val, y_pred_val)
                },
                "model": pipeline
            }

        return results

    def forecast_sales_price(self, model_type: str = 'Linear Regression'):
        """
        Use the trained model to forecast house prices on the test dataset.

        Args:
            model_type (str): Model to use for predictions. Default is 'Linear Regression'.
        """
        if model_type not in self.models:
            raise ValueError(f"Model {model_type} is not trained or available.")

        # Use the selected model to predict
        _, _, _, _, X_test, _ = self.prepare_features()
        predictions = self.models[model_type].predict(X_test)

        # Save predictions to a CSV file
        test_ids = self.test_data["Id"].to_numpy()
        submission = pd.DataFrame({"Id": test_ids, "SalePrice": predictions})
        submission.to_csv("src/real_estate_toolkit/ml_models/outputs/submission.csv", index=False)
