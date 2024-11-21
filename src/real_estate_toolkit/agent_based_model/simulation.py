from enum import Enum, auto
from dataclasses import dataclass
from random import gauss, randint, shuffle
from typing import Any, List, Dict
from .house import House
from .market import HousingMarket
from .consumer import Segment, Consumer


class CleaningMarketMechanism(Enum):
    INCOME_ORDER_DESCENDANT = auto()
    INCOME_ORDER_ASCENDANT = auto()
    RANDOM = auto()


@dataclass
class AnnualIncomeStatistics:
    minimum: float
    average: float
    standard_deviation: float
    maximum: float


@dataclass
class ChildrenRange:
    minimum: int = 0
    maximum: int = 5


@dataclass
class Simulation:
    housing_market_data: List[Dict[str, Any]]
    consumers_number: int
    years: int
    annual_income: AnnualIncomeStatistics
    children_range: ChildrenRange
    cleaning_market_mechanism: CleaningMarketMechanism
    down_payment_percentage: float = 0.2
    saving_rate: float = 0.3
    interest_rate: float = 0.05

    def create_housing_market(self) -> None:
        """
        Initialize market with houses.
        """
        houses = []
        for house_data in self.housing_market_data:
            house = House(
                id=house_data["id"],
                price=house_data["price"],
                area=house_data["area"],
                bedrooms=house_data["bedrooms"],
                year_built=house_data["year_built"],
                quality_score=house_data.get("quality_score"),
                available=house_data.get("available", True),
            )
            houses.append(house)
        self.housing_market = HousingMarket(houses=houses)

    def create_consumers(self) -> None:
        """
        Generate consumer population.
        """
        consumers = []
        for _ in range(self.consumers_number):
            # Generate annual income within the specified range
            while True:
                income = gauss(self.annual_income.average, self.annual_income.standard_deviation)
                if self.annual_income.minimum <= income <= self.annual_income.maximum:
                    break

            # Generate random number of children
            children = randint(self.children_range.minimum, self.children_range.maximum)

            # Randomly assign a segment
            segment = Segment(randint(1, len(Segment)))

            # Create a consumer
            consumer = Consumer(
                id=len(consumers) + 1,
                annual_income=income,
                children_number=children,
                segment=segment,
                savings=0.0,
                saving_rate=self.saving_rate,
                interest_rate=self.interest_rate,
            )
            consumers.append(consumer)

        self.consumers = consumers

    def compute_consumers_savings(self) -> None:
        """
        Calculate savings for all consumers.
        """
        for consumer in self.consumers:
            consumer.compute_savings(self.years)

    def clean_the_market(self) -> None:
        """
        Execute market transactions.
        """
        # Order consumers based on the selected mechanism
        if self.cleaning_market_mechanism == CleaningMarketMechanism.INCOME_ORDER_DESCENDANT:
            self.consumers.sort(key=lambda x: x.annual_income, reverse=True)
        elif self.cleaning_market_mechanism == CleaningMarketMechanism.INCOME_ORDER_ASCENDANT:
            self.consumers.sort(key=lambda x: x.annual_income)
        elif self.cleaning_market_mechanism == CleaningMarketMechanism.RANDOM:
            shuffle(self.consumers)

        # Each consumer attempts to buy a house
        for consumer in self.consumers:
            consumer.buy_a_house(self.housing_market)

    def compute_owners_population_rate(self) -> float:
        """
        Compute the owners population rate after the market is clean.
        """
        owners = sum(1 for consumer in self.consumers if consumer.house is not None)
        return owners / len(self.consumers)

    def compute_houses_availability_rate(self) -> float:
        """
        Compute the houses availability rate after the market is clean.
        """
        available_houses = sum(1 for house in self.housing_market.houses if house.available)
        return available_houses / len(self.housing_market.houses)



