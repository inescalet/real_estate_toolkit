from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Union

@dataclass
class DataLoader:
    """Class for loading and basic processing of real estate data."""
    data_path: Path
    
    def load_data_from_csv(self) -> List[Dict[str, Any]]:
        """Load data from CSV file into a list of dictionaries."""
        return ... # List of dictionaries with the data
    
    def validate_columns(self, required_columns: List[str]) -> bool:
        """Validate that all required columns are present in the dataset."""
        return ... # True if all required columns are present
        