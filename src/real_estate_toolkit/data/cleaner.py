from dataclasses import dataclass
from typing import Dict, List, Any
import re

@dataclass
class Cleaner:
    """Class for cleaning real estate data."""
    data: List[Dict[str, Any]]
    
    def rename_with_best_practices(self) -> None:
        """
        Rename the columns with best practices (e.g., snake_case and descriptive names).
        
        Tasks:
        1. Iterate through all the keys in the dataset (column names).
        2. Apply transformations to ensure the column names follow snake_case conventions:
           - Lowercase all letters.
           - Replace spaces with underscores.
           - Remove special characters, keeping only alphanumeric and underscores.
        3. Update the dataset with new column names.
        """
        if not self.data:
            return  # No data to process
        
        # Extract original column names from the first dictionary in the dataset
        original_columns = list(self.data[0].keys())
        
        # Create a mapping for renamed columns
        renamed_columns = {
            col: re.sub(r'[^a-zA-Z0-9_]', '', col.lower().replace(" ", "_"))
            for col in original_columns
        }
        
        # Apply the mapping to each row in the dataset
        for row in self.data:
            for old_key, new_key in renamed_columns.items():
                if old_key in row:
                    row[new_key] = row.pop(old_key)

    def na_to_none(self) -> List[Dict[str, Any]]:
        """
        Replace occurrences of "NA" with Python's None in the dataset.
        
        Tasks:
        1. Iterate through all rows and columns in the dataset.
        2. Check if any value equals the string "NA" (case-sensitive).
        3. Replace "NA" with None.
        
        Returns:
            List[Dict[str, Any]]: The modified dataset with "NA" replaced by None.
        """
        for row in self.data:
            for key, value in row.items():
                if value == "NA":
                    row[key] = None
        return self.data
