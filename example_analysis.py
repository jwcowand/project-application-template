from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from dateutil import parser
from data_loader import DataLoader  # Ensure the import is correct
from matplotlib.dates import DateFormatter
from model import Issue, Event  # Ensure you have defined these classes appropriately
import config
import warnings

COLOR_PALETTE = {
    "bar": "#4c72b0",
    "pie": ["#55a868", "#c44e52"],
    "hist": "#8172b2",
    "label_bar": "#8c564b",
    "time_series": "#ff7f0e",
    "state_transition": "#2ca02c"
}

class ExampleAnalysis:
    """
    Performs an analysis of GitHub issues and outputs the results.
    """
    
    def __init__(self):
        """
        Initialize with user parameter from config.
        """
        self.USER: str = config.get_parameter('user')

    def run(self):
        """
        Main method to start the analysis.
        """
        # Load and process issues using DataLoader
        data_loader = DataLoader()
        issues_df = data_loader.load_and_process_issues()

        # Check if any issues were loaded
        if issues_df.empty:
            print("No issues found to analyze.")
            return
        
        # Convert DataFrame to list of Issue objects
        issues: List[Issue] = [Issue(row.to_dict()) for _, row in issues_df.iterrows()]

        ### BASIC STATISTICS
        # Calculate the total number of events
        total_events = sum(len(issue.events) for issue in issues)
        
        print(f'\n\nFound {total_events} events across {len(issues)} issues.\n\n')
        
        ### BAR CHART: Top 50 Issue Creators
        top_n = 30
        plt.figure(figsize=(10, 8))
        issues_df['creator'].value_counts().nlargest(top_n).plot(kind="bar", color=COLOR_PALETTE["bar"])
        plt.title(f"Top {top_n} Issue Creators")
        plt.xlabel("Creator Names")
        plt.ylabel("Number of Issues Created")
        plt.xticks(rotation=25, ha="right")  # Rotate x-axis labels for readability
        plt.tight_layout()
        plt.show()

        ### PIE CHART: Issue State Distribution
        plt.figure(figsize=(8, 8))
        state_counts = issues_df['state'].value_counts()
        state_counts.plot(kind="pie", autopct='%1.1f%%', startangle=140, colors=COLOR_PALETTE["pie"], title="Issue State Distribution")
        plt.ylabel("")  # Hide y-axis label for a cleaner look
        plt.show()

        ### BAR CHART: Top 10 Labels Used
        labels = pd.Series([label for labels in issues_df['labels'] for label in labels])
        label_counts = labels.value_counts().nlargest(10)
        plt.figure(figsize=(10, 6))
        label_counts.plot(kind="bar", color=COLOR_PALETTE["label_bar"])
        plt.title("Top 10 Labels Used in Issues")
        plt.xlabel("Label")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

        ### HISTOGRAM: Time to Resolution for Closed Issues
        times_to_resolve = [
            (issue['updated_at'] - issue['created_at']).days
            for _, issue in issues_df.iterrows()
            if issue['state'] == 'closed' and issue['created_at'] and issue['updated_at']
        ]
        
        if times_to_resolve:
            avg_time_to_resolve = sum(times_to_resolve) / len(times_to_resolve)
            print(f"\nAverage Time to Resolve Issues: {avg_time_to_resolve:.2f} days\n")

            # Plot distribution of resolution times
            plt.figure(figsize=(10, 6))
            plt.hist(times_to_resolve, bins=20, color=COLOR_PALETTE["hist"], edgecolor='black')
            plt.title("Distribution of Time to Resolve Issues")
            plt.xlabel("Days to Resolution")
            plt.ylabel("Frequency")
            plt.axvline(avg_time_to_resolve, color='red', linestyle='--', linewidth=1, label=f'Average: {avg_time_to_resolve:.2f} days')
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("No closed issues with valid dates found for time-to-resolution analysis.")
        
        
        warnings.filterwarnings("ignore", message=".*Converting to PeriodArray/Index representation will drop timezone information.*")
        issues_df['created_date'] = pd.to_datetime(issues_df['created_at'])
        issues_df['month'] = issues_df['created_date'].dt.to_period('M')
        monthly_issue_count = issues_df['month'].value_counts().sort_index()

        plt.figure(figsize=(10, 6))
        monthly_issue_count.plot(kind="line", color=COLOR_PALETTE["time_series"], marker='o')
        plt.title("Number of Issues Created Per year")
        plt.xlabel("Year")
        plt.ylabel("Number of Issues Created")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    ExampleAnalysis().run()
