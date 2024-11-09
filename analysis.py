import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
from data_loader import DataLoader

class Analysis:
    def _init_(self):
        """Initialize the Analysis class"""
        pass

    def filter_issues(self, df, label=None, creator=None):
        """Filter issues based on a specified label or creator."""
        # Explode 'labels' column if it is a list, to handle multiple labels per issue
        if 'labels' in df.columns and df['labels'].apply(lambda x: isinstance(x, list)).any():
            df = df.explode('labels')

        filtered_df = df
        if label:
            filtered_df = filtered_df[filtered_df['labels'] == label]
        if creator:
            filtered_df = filtered_df[filtered_df['creator'] == creator]

        print(f"Filtered {len(filtered_df)} issues for label '{label}' and creator '{creator}'")
        return filtered_df
        
    def analyze_and_visualize(self, filtered_df, df):
        """Perform analysis and create visualizations for filtered issues."""
        if filtered_df.empty:
            print("No issues found for the specified label and/or creator. Analysis and visualization skipped.")
            return
        
        # Handle multiple labels in the 'labels' column
        if 'labels' in filtered_df.columns and filtered_df['labels'].apply(lambda x: isinstance(x, list)).any():
            filtered_df = filtered_df.explode('labels')
        
        # Time to Close Analysis (we need 'closed_at' and 'created_at' to calculate this)
        closed_issues = filtered_df.dropna(subset=['closed_at']).copy()
        closed_issues['time_to_close'] = (closed_issues['closed_at'] - closed_issues['created_at']).dt.days

        if closed_issues.empty:
            print("No closed issues found. Average time to close cannot be calculated.")
            avg_time_to_close = float('nan')
        else:
            avg_time_to_close = closed_issues['time_to_close'].mean()
            print(f"Average time to close (days): {avg_time_to_close:.2f}")

        # Visualization: Issues Opened vs Closed by User and Label
        opened_by_user_label = filtered_df.groupby(['creator', 'labels']).size().rename('opened_count')
        closed_by_user_label = closed_issues.groupby(['creator', 'labels']).size().rename('closed_count')
        user_label_counts = filtered_df.groupby('labels').size().sort_values(ascending=False)

        # Check the unique labels used by the creator
        print(f"Unique labels used by {filtered_df['creator'].iloc[0]}: {user_label_counts.index.tolist()}")

        if user_label_counts.empty:
            print(f"No labels found for user '{filtered_df['creator'].iloc[0]}'.")
            return
        # Combine opened and closed counts into a single DataFrame
        user_label_issue_counts = pd.concat([opened_by_user_label, closed_by_user_label], axis=1).fillna(0).astype(int)

        if user_label_issue_counts.empty:
            print("No data available for opened/closed issues by user and label. Plotting skipped.")
            return

        # Plotting opened vs closed issues per user and label
        ax = user_label_issue_counts.plot(kind='bar', stacked=False, figsize=(14, 8), color=['skyblue', 'salmon'])
        plt.title('Number of Issues Opened and Closed by User and Label')
        plt.xlabel('User and Label')
        plt.ylabel('Issue Count')
        plt.legend(['Opened Issues', 'Closed Issues'])
        plt.xticks(rotation=45)
        plt.ylim(0, 5)  # Set y-axis limits to between 0 and 5 for better clarity
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Ensure the y-axis only shows integer values
        ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

        plt.show()

        # Now, to visualize the labels used by that particular user
        # Filter only for the creator user and calculate the frequency of each label for that user
        user_label_counts = filtered_df.groupby('labels').size().sort_values(ascending=False)

        if user_label_counts.empty:
            print(f"No labels found for user '{filtered_df['creator'].iloc[0]}'.")
            return

        # Plotting labels used by the user
        plt.figure(figsize=(14, 8))
        user_label_counts.plot(kind='bar', color='lightcoral')
        plt.title(f'Labels Used by {filtered_df["creator"].iloc[0]}')
        plt.xlabel('Labels')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()



def parse_args():
    """Parse command line arguments."""
    import argparse
    parser = argparse.ArgumentParser(description="GitHub Issues Analysis")
    parser.add_argument('--label', type=str, help="Filter by issue label")
    parser.add_argument('--creator', type=str, help="Filter by issue creator")
    return parser.parse_args()

def main():
    # Initialize the DataLoader and load & process issues
    data_loader = DataLoader()  # DataLoader will automatically handle the configuration and file loading
    df = data_loader.load_and_process_issues()  # Load and process the issues using DataLoader

    # Parse command-line arguments
    args = parse_args()  # Get command-line arguments for filtering
    label = args.label  # Use label from arguments or None if not provided
    creator = args.creator  # Use creator from args or None if not provided
    
    # Initialize and run analysis
    analysis = Analysis()  # No need to pass df to the constructor
    filtered_df = analysis.filter_issues(df, label=label, creator=creator)  # Pass df to filter_issues method
    analysis.analyze_and_visualize(filtered_df, df)  # Perform analysis and visualization

if __name__ == "_main_":
    main()