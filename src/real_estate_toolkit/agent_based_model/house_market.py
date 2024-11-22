from typing import List, Optional
from .house import House


class HousingMarket:
    """Class for managing a collection of houses and market-wide operations."""
    
    def __init__(self, houses: List[House]):
        """
        Initialize the housing market with a list of houses.
        
        Args:
            houses (List[House]): List of House objects in the market.
        """
        self.houses: List[House] = houses

    def get_house_by_id(self, house_id: int) -> Optional[House]:
        """
        Retrieve a specific house by its unique ID.

        Args:
            house_id (int): The ID of the house to retrieve.
        
        Returns:
            Optional[House]: The House object with the given ID, or None if not found.
        
        Raises:
            ValueError: If the house ID does not exist.
        """
        for house in self.houses:
            if house.id == house_id:
                return house
        raise ValueError(f"House with ID {house_id} not found.")

    def calculate_average_price(self, bedrooms: Optional[int] = None) -> float:
        """
        Calculate the average price of houses in the market, optionally filtered by bedrooms.

        Args:
            bedrooms (Optional[int]): Number of bedrooms to filter by. If None, consider all houses.
        
        Returns:
            float: The average price of the filtered houses. Returns 0 if no matching houses are found.
        """
        # Filter houses based on the number of bedrooms if specified
        filtered_houses = (
            [house for house in self.houses if house.bedrooms == bedrooms]
            if bedrooms is not None
            else self.houses
        )

        # Handle the case of no matching houses
        if not filtered_houses:
            return 0.0

        # Calculate the average price
        total_price = sum(house.price for house in filtered_houses)
        return total_price / len(filtered_houses)

    def get_houses_that_meet_requirements(self, max_price: int, segment: str) -> Optional[List[House]]:
        """
        Filter houses based on buyer requirements.

        Args:
            max_price (int): The maximum price the buyer is willing to pay.
            segment (str): The segment criteria (e.g., "FANCY", "OPTIMIZER", "AVERAGE").

        Returns:
            Optional[List[House]]: List of houses that meet the requirements, or an empty list if none match.
        """
        segment_filters = {
            "FANCY": lambda house: house.quality_score and house.quality_score.value >= 4,
            "OPTIMIZER": lambda house: house.calculate_price_per_square_foot() < max_price / house.area if house.area > 0 else False,
            "AVERAGE": lambda house: house.price <= max_price,
        }

        # Validate the segment
        if segment not in segment_filters:
            raise ValueError(f"Invalid segment: {segment}. Choose from 'FANCY', 'OPTIMIZER', or 'AVERAGE'.")

        # Filter houses based on criteria
        matching_houses = [
            house for house in self.houses
            if house.available and house.price <= max_price and segment_filters[segment](house)
        ]

        return matching_houses if matching_houses else []

