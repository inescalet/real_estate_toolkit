from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List
from .house import House
from .market import HousingMarket

class Segment(Enum):
    FANCY = auto()  # Prefers new construction with the highest quality score
    OPTIMIZER = auto()  # Focuses on price per square foot value
    AVERAGE = auto()  # Considers houses below the average market price

@dataclass
class Consumer:
    id: int
    annual_income: float
    children_number: int
    segment: Segment
    house: Optional[House] = None
    savings: float = 0.0
    saving_rate: float = 0.3
    interest_rate: float = 0.05

    def compute_savings(self, years: int) -> None:
        """
        Calculate accumulated savings over time using compound interest.
        """
        annual_savings = self.annual_income * self.saving_rate
        self.savings = annual_savings * ((1 + self.interest_rate) ** years - 1) / self.interest_rate

compute_savings:
•	Calcula los ahorros acumulados usando la fórmula de interés compuesto.
•	Considera el ahorro anual (annual_income×saving_rateannual_income×saving_rate) y el tiempo en años.


    def buy_a_house(self, housing_market: HousingMarket) -> None:
        """
        Attempt to purchase a suitable house based on the consumer's segment and financial resources.
        """
        suitable_houses = []

        # Find houses based on segment
        if self.segment == Segment.FANCY:
            suitable_houses = [
                house for house in housing_market.houses
                if house.available and house.is_new_construction() and house.quality_score == 5
            ]
        elif self.segment == Segment.OPTIMIZER:
            suitable_houses = [
                house for house in housing_market.houses
                if house.available and house.calculate_price_per_square_foot() <= (self.annual_income / 12)
            ]
        elif self.segment == Segment.AVERAGE:
            avg_price = housing_market.calculate_average_price()
            suitable_houses = [
                house for house in housing_market.houses
                if house.available and house.price <= avg_price
            ]

        # Attempt to buy the first suitable house
        for house in suitable_houses:
            if self.savings >= house.price:
                self.house = house
                house.sell_house()
                self.savings -= house.price
                print(f"Consumer {self.id} bought house {house.id} for ${house.price}.")
                return

        print(f"Consumer {self.id} could not find a suitable house to buy.")
