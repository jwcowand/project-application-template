from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from dateutil import parser

from data_loader import DataLoader  # Ensure the import is correct
from model import Issue, Event  # Ensure you have defined these classes appropriately
import config

class ExampleAnalysis:
    """
    Implements an example analysis of GitHub issues and outputs the result of that analysis.
    """
    
    def __init__(self):
        """
        Constructor
        """
        # Parameter is passed in via command line (--user)
        self.USER: str = config.get_parameter('user')

    def run(self):
        """
        Starting point for this analysis.
        """
        # Use the DataLoader to load and process issues
        data_loader = DataLoader()
        issues_df = data_loader.load_and_process_issues()

        # Check if issues were loaded correctly
        if issues_df.empty:
            print("No issues found to analyze.")
            return
        
        # Convert DataFrame to list of Issue objects
        issues: List[Issue] = [Issue(row.to_dict()) for index, row in issues_df.iterrows()]

        ### BASIC STATISTICS
        # Calculate the total number of events for a specific user (if specified in command line args)
        total_events: int = 0
        for issue in issues:
            total_events += len([e for e in issue.events if self.USER is None or e.author == self.USER])
        
        output: str = f'Found {total_events} events across {len(issues)} issues'
        if self.USER is not None:
            output += f' for {self.USER}.'
        else:
            output += '.'
        print('\n\n' + output + '\n\n')
        
        ### BAR CHART
        # Display a graph of the top 50 creators of issues
        top_n: int = 50
        df_hist = issues_df['creator'].value_counts().nlargest(top_n).plot(kind="bar", figsize=(14, 8), title=f"Top {top_n} issue creators")
        df_hist.set_xlabel("Creator Names")
        df_hist.set_ylabel("# of issues created")
        plt.show() 

        ### ISSUE STATE DISTRIBUTION
        # Display the distribution of open and closed issues
        state_counts = issues_df['state'].value_counts()
        state_counts.plot(kind="pie", autopct='%1.1f%%', startangle=140, title="Issue State Distribution", figsize=(8, 8))
        plt.ylabel("")  # Hide the y-axis label for better readability
        plt.show()

        ### LABEL ANALYSIS
        # Analyze the frequency of labels across issues
        labels = pd.Series([label for labels in issues_df['labels'] for label in labels])
        label_counts = labels.value_counts().nlargest(10)  # Display the top 10 labels
        label_counts.plot(kind="bar", figsize=(10, 6), title="Top 10 Labels Used in Issues")
        plt.xlabel("Label")
        plt.ylabel("Frequency")
        plt.show()

        ### TIME TO RESOLUTION ANALYSIS
        # Calculate average time to resolution for closed issues
        times_to_resolve = []
        for index, issue in issues_df.iterrows():
            if issue['state'] == 'closed' and issue['created_at'] and issue['updated_at']:
                created_at = issue['created_at']
                updated_at = issue['updated_at']
                times_to_resolve.append((updated_at - created_at).days)
        
        if times_to_resolve:
            avg_time_to_resolve = sum(times_to_resolve) / len(times_to_resolve)
            print(f"\nAverage Time to Resolve Issues: {avg_time_to_resolve:.2f} days\n")

            # Plotting the distribution of resolution times
            plt.hist(times_to_resolve, bins=20, color='skyblue', edgecolor='black')
            plt.title("Distribution of Time to Resolve Issues")
            plt.xlabel("Days to Resolution")
            plt.ylabel("Frequency")
            plt.show()
        else:
            print("No closed issues with valid dates found for time-to-resolution analysis.")

if __name__ == '__main__':
    # Invoke run method when running this module directly
    ExampleAnalysis().run()
