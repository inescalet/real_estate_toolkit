import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Union, Any


@dataclass
class DescriptorNumpy:
    """Class for summarizing and describing real estate data using NumPy."""
    data: np.ndarray
    columns: List[str]  # Column names for the data array

    def none_ratio(self, columns: List[str] = "all") -> Dict[str, float]:
        """
        Compute the ratio of None (or NaN) values for each specified column.
        If 'columns' is 'all', it calculates the ratio for all columns.
        
        Args:
            columns (List[str]): List of column names to analyze. Default is "all".
        
        Returns:
            Dict[str, float]: A dictionary where keys are column names and values are the None ratio.
        """
        if columns == "all":
            columns = self.columns  # Use all columns if none are specified.

        result = {}
        for col in columns:
            if col not in self.columns:
                raise ValueError(f"Column {col} not found in data")  # Validate column exists.

            col_idx = self.columns.index(col)  # Get the index of the column.
            col_data = self.data[:, col_idx]  # Select the data for the column.

            none_count = np.isnan(col_data).sum()  # Count NaN values in the column.
            result[col] = none_count / len(col_data)  # Calculate the proportion of missing values.
        return result

    def average(self, columns: List[str] = "all") -> Dict[str, float]:
        """
        Compute the average value for specified columns, ignoring NaN values.

        Args:
            columns (List[str]): List of column names to calculate the average for. Default is "all".

        Returns:
            Dict[str, float]: A dictionary where keys are column names and values are their averages.
        """
        if columns == "all":
            columns = self.columns  # Use all columns if none are specified.

        result = {}
        for col in columns:
            if col not in self.columns:
                raise ValueError(f"Column {col} not found in data")  # Validate column exists.

            col_idx = self.columns.index(col)  # Get the index of the column.
            col_data = self.data[:, col_idx].astype(float)  # Ensure the data is numeric.

            result[col] = np.nanmean(col_data)  # Calculate the mean, ignoring NaN values.
        return result

    def median(self, columns: List[str] = "all") -> Dict[str, float]:
        """
        Compute the median value for numeric columns, ignoring NaN values.

        Args:
            columns (List[str]): List of column names to calculate the median for. Default is "all".

        Returns:
            Dict[str, float]: A dictionary where keys are column names and values are their medians.
        """
        if columns == "all":
            columns = self.columns  # Use all columns if none are specified.
        
        result = {}
        for col in columns:
            if col not in self.columns:
                raise ValueError(f"Column {col} not found in data")  # Validate column exists.
            col_idx = self.columns.index(col)  # Get the index of the column.
            col_data = self.data[:, col_idx].astype(float)  # Ensure the data is numeric.
            result[col] = np.nanmedian(col_data)  # Calculate the median, ignoring NaN values.
        return result

    def percentile(self, columns: List[str] = "all", percentile: int = 50) -> Dict[str, float]:
        """
        Compute the specified percentile for numeric columns, ignoring NaN values.

        Args:
            columns (List[str]): List of column names to calculate the percentile for. Default is "all".
            percentile (int): The percentile to compute (e.g., 25 for the 25th percentile). Default is 50.

        Returns:
            Dict[str, float]: A dictionary where keys are column names and values are their computed percentiles.
        """
        if columns == "all":
            columns = self.columns  # Use all columns if none are specified.
        
        result = {}
        for col in columns:
            if col not in self.columns:
                raise ValueError(f"Column {col} not found in data")  # Validate column exists.
            col_idx = self.columns.index(col)  # Get the index of the column.
            col_data = self.data[:, col_idx].astype(float)  # Ensure the data is numeric.
            result[col] = np.nanpercentile(col_data, percentile)  # Calculate the percentile, ignoring NaN values.
        return result
