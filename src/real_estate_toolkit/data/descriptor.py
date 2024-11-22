
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union, Any
import statistics
import numpy as np

@dataclass
class Descriptor:
    """Class for summarizing and describing real estate data."""
    data: List[Dict[str, Any]]

    def none_ratio(self, columns: List[str] = "all") -> Dict[str, float]:
        """
        Compute the ratio of None values per column.
        
        Args:
            columns (List[str]): List of columns to compute the ratio. Default is "all".
        
        Returns:
            Dict[str, float]: Dictionary with column names as keys and None ratio as values.
        
        Raises:
            ValueError: If any specified column does not exist in the data.
        """
        # If "all", compute for all columns
        if columns == "all":
            columns = self.data[0].keys() if self.data else []
        
        # Validate column names
        for col in columns:
            if col not in self.data[0]:
                raise ValueError(f"Column '{col}' not found in data.")

        # Compute None ratios
        none_ratios = {}
        for col in columns:
            total_values = len(self.data)
            none_count = sum(1 for row in self.data if row.get(col) is None)
            none_ratios[col] = none_count / total_values if total_values > 0 else 0
        
        return none_ratios

    def average(self, columns: List[str] = "all") -> Dict[str, float]:
        """
        Compute the average value for numeric variables, ignoring None values.
        
        Args:
            columns (List[str]): List of columns to compute the average. Default is "all".
        
        Returns:
            Dict[str, float]: Dictionary with column names as keys and average values as values.
        
        Raises:
            ValueError: If any specified column does not exist or is not numeric.
        """
        # If "all", compute for all numeric columns
        if columns == "all":
            columns = [col for col in self.data[0].keys() if isinstance(self.data[0][col], (int, float))]

        averages = {}
        for col in columns:
            try:
                values = [row[col] for row in self.data if row.get(col) is not None]
                averages[col] = sum(values) / len(values) if values else 0
            except KeyError:
                raise ValueError(f"Column '{col}' not found in data or is not numeric.")
        
        return averages

    def median(self, columns: List[str] = "all") -> Dict[str, float]:
        """
        Compute the median value for numeric variables, ignoring None values.
        
        Args:
            columns (List[str]): List of columns to compute the median. Default is "all".
        
        Returns:
            Dict[str, float]: Dictionary with column names as keys and median values as values.
        """
        # If "all", compute for all numeric columns
        if columns == "all":
            columns = [col for col in self.data[0].keys() if isinstance(self.data[0][col], (int, float))]

        medians = {}
        for col in columns:
            try:
                values = sorted(row[col] for row in self.data if row.get(col) is not None)
                medians[col] = statistics.median(values) if values else 0
            except KeyError:
                raise ValueError(f"Column '{col}' not found in data or is not numeric.")
        
        return medians

    def percentile(self, columns: List[str] = "all", percentile: int = 50) -> Dict[str, float]:
        """
        Compute a specific percentile value for numeric variables, ignoring None values.
        
        Args:
            columns (List[str]): List of columns to compute the percentile. Default is "all".
            percentile (int): Percentile to compute. Default is 50 (median).
        
        Returns:
            Dict[str, float]: Dictionary with column names as keys and percentile values as values.
        """
        # If "all", compute for all numeric columns
        if columns == "all":
            columns = [col for col in self.data[0].keys() if isinstance(self.data[0][col], (int, float))]

        percentiles = {}
        for col in columns:
            try:
                values = sorted(row[col] for row in self.data if row.get(col) is not None)
                k = (len(values) - 1) * (percentile / 100)
                f = int(k)
                c = min(f + 1, len(values) - 1)
                percentiles[col] = (values[f] + (values[c] - values[f]) * (k - f)) if values else 0
            except KeyError:
                raise ValueError(f"Column '{col}' not found in data or is not numeric.")
        
        return percentiles

    def type_and_mode(self, columns: List[str] = "all") -> Dict[str, Union[Tuple[str, float], Tuple[str, str]]]:
        """
        Compute the mode for variables and their type, ignoring None values.
        
        Args:
            columns (List[str]): List of columns to compute the mode. Default is "all".
        
        Returns:
            Dict[str, Union[Tuple[str, float], Tuple[str, str]]]: 
                Dictionary with column names as keys and tuples (type, mode) as values.
        """
        # If "all", compute for all columns
        if columns == "all":
            columns = self.data[0].keys()

        modes = {}
        for col in columns:
            try:
                values = [row[col] for row in self.data if row.get(col) is not None]
                if not values:
                    modes[col] = ("unknown", None)
                    continue
                
                value_counts = {val: values.count(val) for val in set(values)}
                mode = max(value_counts, key=value_counts.get)
                modes[col] = (type(mode).__name__, mode)
            except KeyError:
                raise ValueError(f"Column '{col}' not found in data.")
        
        return modes

@dataclass
class DescriptorNumpy:
    """Class for summarizing and describing real estate data using NumPy."""
    data: np.ndarray  # Expect a structured NumPy array or ndarray

    def none_ratio(self, columns: List[str] = "all") -> Dict[str, float]:
        """
        Compute the ratio of None (or NaN) values per column.
        
        Args:
            columns (List[str]): List of column names to compute ratios for. Default is "all".
        
        Returns:
            Dict[str, float]: Dictionary with column names as keys and None ratios as values.
        """
        if columns == "all":
            columns = self.data.dtype.names  # Use all columns in the structured array

        none_ratios = {}
        for col in columns:
            if col not in self.data.dtype.names:
                raise ValueError(f"Column '{col}' not found in data.")
            
            column_data = self.data[col]
            none_ratios[col] = np.isnan(column_data).sum() / len(column_data)
        
        return none_ratios

    def average(self, columns: List[str] = "all") -> Dict[str, float]:
        """
        Compute the average value for numeric variables, ignoring NaN values.
        
        Args:
            columns (List[str]): List of column names to compute averages for. Default is "all".
        
        Returns:
            Dict[str, float]: Dictionary with column names as keys and average values as values.
        """
        if columns == "all":
            columns = [col for col in self.data.dtype.names if self.data[col].dtype.kind in 'if']

        averages = {}
        for col in columns:
            if col not in self.data.dtype.names:
                raise ValueError(f"Column '{col}' not found in data or is not numeric.")
            
            column_data = self.data[col]
            averages[col] = np.nanmean(column_data)  # Ignore NaN values during computation
        
        return averages

    def median(self, columns: List[str] = "all") -> Dict[str, float]:
        """
        Compute the median value for numeric variables, ignoring NaN values.
        
        Args:
            columns (List[str]): List of column names to compute medians for. Default is "all".
        
        Returns:
            Dict[str, float]: Dictionary with column names as keys and median values as values.
        """
        if columns == "all":
            columns = [col for col in self.data.dtype.names if self.data[col].dtype.kind in 'if']

        medians = {}
        for col in columns:
            if col not in self.data.dtype.names:
                raise ValueError(f"Column '{col}' not found in data or is not numeric.")
            
            column_data = self.data[col]
            medians[col] = np.nanmedian(column_data)  # Ignore NaN values during computation
        
        return medians

    def percentile(self, columns: List[str] = "all", percentile: int = 50) -> Dict[str, float]:
        """
        Compute a specific percentile value for numeric variables, ignoring NaN values.
        
        Args:
            columns (List[str]): List of column names to compute percentiles for. Default is "all".
            percentile (int): Percentile to compute. Default is 50 (median).
        
        Returns:
            Dict[str, float]: Dictionary with column names as keys and percentile values as values.
        """
        if columns == "all":
            columns = [col for col in self.data.dtype.names if self.data[col].dtype.kind in 'if']

        percentiles = {}
        for col in columns:
            if col not in self.data.dtype.names:
                raise ValueError(f"Column '{col}' not found in data or is not numeric.")
            
            column_data = self.data[col]
            percentiles[col] = np.nanpercentile(column_data, percentile)  # Handle NaN values
        
        return percentiles

    def type_and_mode(self, columns: List[str] = "all") -> Dict[str, Union[Tuple[str, float], Tuple[str, str]]]:
        """
        Compute the mode and type for variables, ignoring NaN values.
        
        Args:
            columns (List[str]): List of column names to compute mode and type for. Default is "all".
        
        Returns:
            Dict[str, Union[Tuple[str, float], Tuple[str, str]]]:
                Dictionary with column names as keys and tuples (type, mode) as values.
        """
        if columns == "all":
            columns = self.data.dtype.names

        modes = {}
        for col in columns:
            if col not in self.data.dtype.names:
                raise ValueError(f"Column '{col}' not found in data.")

            column_data = self.data[col]
            unique, counts = np.unique(column_data[~np.isnan(column_data)], return_counts=True)
            if len(unique) == 0:  # If no valid data
                modes[col] = ("unknown", None)
                continue
            
            mode = unique[np.argmax(counts)]  # Most frequent value
            modes[col] = (column_data.dtype.name, mode)
        
        return modes
