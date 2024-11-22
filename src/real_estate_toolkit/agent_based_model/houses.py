from enum import Enum
from dataclasses import dataclass
from typing import Optional


class QualityScore(Enum):
    """Enum representing the quality score of a house."""
    EXCELLENT = 5
    GOOD = 4
    AVERAGE = 3
    FAIR = 2
    POOR = 1


@dataclass
class House:
    """Class representing an individual property in the real estate market."""
    id: int
    price: float
    area: float  # Square footage
    bedrooms: int
    year_built: int
    quality_score: Optional[QualityScore] = None
    available: bool = True  # Default: House is available for sale

    def calculate_price_per_square_foot(self) -> float:
        """
        Calculate and return the price per square foot.
        
        Returns:
            float: Price per square foot rounded to 2 decimal places.
        """
        if self.area == 0:
            raise ValueError("Area cannot be zero when calculating price per square foot.")
        return round(self.price / self.area, 2)

    def is_new_construction(self, current_year: int = 2024) -> bool:
        """
        Determine if the house is considered new construction (< 5 years old).

        Args:
            current_year (int): The current year to compare with year_built.

        Returns:
            bool: True if the house is less than 5 years old, False otherwise.
        """
        return (current_year - self.year_built) < 5

    def get_quality_score(self) -> None:
        """
        Generate a quality score for the house if it is not already set.
        
        - Considers house age, size (area), and number of bedrooms.
        - Assigns a meaningful score based on these attributes.
        """
        if self.quality_score is not None:
            return  # Quality score is already set
        
        # Example scoring logic
        age = 2024 - self.year_built
        if age < 5:
            base_score = 5
        elif age < 15:
            base_score = 4
        elif age < 30:
            base_score = 3
        elif age < 50:
            base_score = 2
        else:
            base_score = 1

        # Adjust based on size and bedrooms
        size_bonus = 1 if self.area > 2000 else 0
        bedroom_bonus = 1 if self.bedrooms > 3 else 0

        # Set the final quality score
        total_score = base_score + size_bonus + bedroom_bonus
        self.quality_score = QualityScore(min(total_score, 5))  # Cap score at 5

    def sell_house(self) -> None:
        """
        Mark the house as sold by setting `available` to False.
        """
        self.available = False
