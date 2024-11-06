from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from dateutil import parser

from data_loader import DataLoader  # Ensure the import is correct
from model import Issue, Event  # Ensure you have defined these classes appropriately
import config

class MonthIssueAnalysis:
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
        ###BAR CHART
        #Display a graph of every months open and closed issues
        opened_issue_month = []
        for index, issue in issues_df.iterrows():
            if issue['created_at'].month:
                if not pd.isna(issue['created_at'].month):
                    created_at = issue['created_at'].month
                    opened_issue_month.append(created_at)
        closed_issue_month = []
        for index, issue in issues_df.iterrows():
            if issue['closed_at'].month and issue.get('state') == 'closed': #and statement to ensure no nan's are appeneded
                if not pd.isna(issue['closed_at'].month):  
                    closed_at = issue['closed_at'].month
                    closed_issue_month.append(closed_at)
        
        if opened_issue_month and closed_issue_month:
            # Plotting the distribution of resolution times
            plt.hist([opened_issue_month, closed_issue_month],bins=range(1,14), align='left', edgecolor='black', label= ['Opened Issues','Closed Issues'])
            plt.title("Distribution of Open/Closed Issues Per Month")
            plt.legend(loc='upper right')
            plt.xlabel("Months")
            plt.ylabel("Number of Issues")
            plt.xticks(range(1,13))
            plt.show()

if __name__ == '__main__':
    # Invoke run method when running this module directly
    MonthIssueAnalysis().run()
