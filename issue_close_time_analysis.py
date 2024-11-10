import matplotlib.pyplot as plt
import pandas as pd
from data_loader import DataLoader
import config

class IssueCloseTimeAnalysis:
    """
    Analyzes GitHub issues by calculating the average time to close each issue type. Ignores non closed issues and those without a close time.
    """
    
    def __init__(self):
        """
        Constructor
        """
        # Parameter is passed in via command line (--user), unused in this analysis
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

        # Get only closed issues so we can analyze the close time, ignores missing times for close_at
        closed_issues_df = issues_df[issues_df['state'] == 'closed']
        closed_issues_df = closed_issues_df.dropna(subset=['closed_at'])

        # Calculate the close time
        closed_issues_df['close_time'] = closed_issues_df['closed_at'] - closed_issues_df['created_at']

        # Get unique labels across all issues
        unique_labels = set(label for sublist in closed_issues_df['labels'] for label in sublist)

        # Create a dictionary to store DataFrames for each label
        label_dfs = {}

        for label in unique_labels:
            # Filter rows that contain the current label
            label_dfs[label] = closed_issues_df[closed_issues_df['labels'].apply(lambda x: label in x)].reset_index(drop=True)

        label_close_times = {label: [] for label in unique_labels}
        # For each issue, add its close time to the corresponding label(s)
        
        for index, row in closed_issues_df.iterrows():
            for label in row['labels']:
                label_close_times[label].append(row['close_time'])

        # Calculate the average close time for each label
        average_close_times = {label: pd.to_timedelta(sum(times, pd.Timedelta(0)) / len(times)) for label, times in label_close_times.items()}

        # Display the average close time for each label
        for label, avg_close_time in average_close_times.items():
            print(f"Average Close Time for label '{label}': {avg_close_time}")

        # Sort the labels alphabetically
        sorted_labels = sorted(average_close_times.keys())

        #convert to days (86400 seconds in 1 day)
        average_times_in_days = [avg_time.total_seconds() / 86400 for avg_time in average_close_times.values()]

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.bar(sorted_labels, average_times_in_days, color='skyblue')

        # Add labels and title
        plt.xlabel('Label')
        plt.ylabel('Average Close Time (days)')
        plt.title('Average Close Time for Each Label')
        plt.xticks(rotation=45, ha='right')  # Rotate labels for better visibility

        # Display the plot
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    # Invoke run method when running this module directly
    IssueCloseTimeAnalysis().run()
