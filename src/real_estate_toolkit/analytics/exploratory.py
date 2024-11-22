from typing import List, Dict, Any, Optional
import polars as pl
import plotly.express as px
from pathlib import Path

class MarketAnalyzer:
    def __init__(self, data_path: str):
        """
        Initialize the analyzer with data from a CSV file.
        
        Args:
            data_path (str): Path to the Ames Housing dataset.
        """
        self.data_path = data_path
        # Load raw real estate data using Polars
        self.real_state_data = pl.read_csv(data_path)
        # Placeholder for cleaned data
        self.real_state_clean_data = None

    def clean_data(self) -> None:
        """
        Perform comprehensive data cleaning:
        
        1. Handle missing values:
           - Fill specific columns with mean/median or default values.
        2. Convert columns to appropriate data types.
           - Ensure numeric columns are numeric.
           - Ensure categorical columns are categorized.
        """
        # Handle missing values
        clean_data = self.real_state_data.with_columns([
            pl.col("LotFrontage").fill_null(strategy="mean"),  # Fill with mean
            pl.col("GarageYrBlt").fill_null(strategy="median"),  # Fill with median
            pl.col("MasVnrType").fill_null("None")  # Fill with "None" for missing masonry veneer types
        ])
        
        # Drop rows with missing target variable `SalePrice`
        clean_data = clean_data.drop_nulls(subset=["SalePrice"])
        
        # Convert columns to appropriate types
        clean_data = clean_data.with_columns([
            pl.col("YearBuilt").cast(pl.Int32),  # Ensure year is an integer
            pl.col("Neighborhood").cast(pl.Categorical)  # Convert neighborhood to categorical
        ])
        
        # Assign cleaned data to the class property
        self.real_state_clean_data = clean_data

    def generate_price_distribution_analysis(self) -> pl.DataFrame:
        """
        Analyze sale price distribution using clean data.
        
        1. Compute basic price statistics.
        2. Create an interactive histogram of sale prices.

        Returns:
            pl.DataFrame: A dataframe with price statistics.
        """
        # Compute basic price statistics
        price_statistics = self.real_state_clean_data.select([
            pl.col("SalePrice").mean().alias("mean"),
            pl.col("SalePrice").median().alias("median"),
            pl.col("SalePrice").std().alias("std_dev"),
            pl.col("SalePrice").min().alias("min"),
            pl.col("SalePrice").max().alias("max")
        ])
        
        # Create an interactive histogram of sale prices
        fig = px.histogram(
            self.real_state_clean_data.to_pandas(),  # Convert to pandas for Plotly
            x="SalePrice",
            title="Distribution of Sale Prices",
            nbins=50,
            labels={"SalePrice": "Sale Price"}
        )
        # Save the figure as an HTML file
        fig.write_html("src/real_estate_toolkit/analytics/outputs/price_distribution.html")
        
        return price_statistics

    def neighborhood_price_comparison(self) -> pl.DataFrame:
        """
        Create a boxplot comparing house prices across different neighborhoods.
        
        1. Group data by neighborhood and calculate price statistics.
        2. Create a Plotly boxplot.

        Returns:
            pl.DataFrame: A dataframe with neighborhood price statistics.
        """
        # Group data by neighborhood and calculate statistics
        neighborhood_stats = self.real_state_clean_data.groupby("Neighborhood").agg([
            pl.col("SalePrice").mean().alias("mean_price"),
            pl.col("SalePrice").median().alias("median_price"),
            pl.col("SalePrice").std().alias("std_dev_price")
        ])
        
        # Create an interactive boxplot
        fig = px.box(
            self.real_state_clean_data.to_pandas(),
            x="Neighborhood",
            y="SalePrice",
            title="Neighborhood Price Comparison",
            labels={"Neighborhood": "Neighborhood", "SalePrice": "Sale Price"},
            color="Neighborhood"
        )
        # Sort neighborhoods by total median price
        fig.update_layout(xaxis={"categoryorder": "total descending"})
        # Save the figure as an HTML file
        fig.write_html("src/real_estate_toolkit/analytics/outputs/neighborhood_prices.html")
        
        return neighborhood_stats

    def feature_correlation_heatmap(self, variables: List[str]) -> None:
        """
        Generate a correlation heatmap for the selected variables.
        
        Args:
            variables (List[str]): List of numerical variables to include in the heatmap.
        """
        # Select only the desired variables
        data = self.real_state_clean_data.select(variables)
        # Compute the correlation matrix
        correlation_matrix = data.corr()
        
        # Create a heatmap using Plotly
        fig = px.imshow(
            correlation_matrix.to_numpy(),
            labels=dict(x=variables, y=variables),
            x=variables,
            y=variables,
            title="Correlation Heatmap"
        )
        # Save the figure as an HTML file
        fig.write_html("src/real_estate_toolkit/analytics/outputs/correlation_heatmap.html")

    def create_scatter_plots(self) -> Dict[str, px.Figure]:
        """
        Create scatter plots exploring relationships between key features.
        
        Scatter plots:
            1. Sale Price vs. Total square footage.
            2. Sale Price vs. Year built.
            3. Overall quality vs. Sale Price.

        Returns:
            Dict[str, px.Figure]: A dictionary with scatter plot figures.
        """
        scatter_plots = {}
        data = self.real_state_clean_data.to_pandas()  # Convert to pandas for Plotly compatibility
        
        # Define relationships to plot
        plots = [
            ("GrLivArea", "SalePrice", "Living Area vs. Sale Price"),
            ("YearBuilt", "SalePrice", "Year Built vs. Sale Price"),
            ("OverallQual", "SalePrice", "Overall Quality vs. Sale Price")
        ]
        
        for x, y, title in plots:
            # Create scatter plot with trendline
            fig = px.scatter(
                data, x=x, y=y,
                title=title,
                labels={x: x, y: y},
                trendline="ols",
                color="Neighborhood",  # Color by neighborhood
                hover_data=["Neighborhood"]  # Show neighborhood in hover info
            )
            # Generate file name and save
            file_name = f"{x}_vs_{y}.html".lower()
            fig.write_html(f"src/real_estate_toolkit/analytics/outputs/{file_name}")
            scatter_plots[title] = fig
        
        return scatter_plots
