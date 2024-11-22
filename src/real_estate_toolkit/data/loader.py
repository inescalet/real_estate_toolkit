from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Union, Any
import polars as pl

@dataclass
class DataLoader:
    """Class for loading and basic processing of real estate data."""
    data_path: Path
    
    def load_data_from_csv(self) -> List[Dict[str, Any]]:
        """
        Load data from CSV file into a list of dictionaries.
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries with the data.

        Raises:
            FileNotFoundError: If the data file is not found.
            ValueError: If there is an error loading the data.
        """
        # Check if the data file exists
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        try:
            # Use Polars to read the CSV file
            df = pl.read_csv(self.data_path)
            # Convert the Polars DataFrame to a list of dictionaries
            return df.to_dicts()
        except Exception as e:
            raise ValueError(f"Error loading data: {e}")
        
    def validate_columns(self, required_columns: List[str]) -> bool:
        """Validate that all required columns are present in the dataset.
        
        Args:
            required_columns (List[str]): List of required column names.
        
        Returns:
            bool: True if all required columns are present, False otherwise.

        Raises:
            FileNotFoundError: If the data file does not exist.
            ValueError: If there is an error reading the CSV file.
        """
        # Check if the file exists
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        # Read the CSV file
        try:
            df = pl.read_csv(self.data_path)
            actual_columns = set(df.columns) # Get columns from the dataset
            # Check if all required columns are present
            return all(column in actual_columns for column in required_columns)
            # Returns True if all required columns are present
        except Exception as e:
            raise ValueError(f"Error validating columns in {self.data_path}: {e}
    