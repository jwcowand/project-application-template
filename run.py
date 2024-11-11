

"""
Starting point of the application. This module is invoked from
the command line to run the analyses.
"""

import argparse

import config
from overall_analysis import OverallAnalysis
from month_issue_analysis import MonthIssueAnalysis
from issue_close_time_analysis import IssueCloseTimeAnalysis
from data_loader import DataLoader
from analysis import Analysis

def parse_args():
    """
    Parses the command line arguments that were provided along
    with the python command. The --feature flag must be provided as
    that determines what analysis to run. Optionally, you can pass in
    a user and/or a label to run analysis focusing on specific issues.
    
    You can also add more command line arguments following the pattern
    below.
    """
    ap = argparse.ArgumentParser("run.py")
    
    # Required parameter specifying what analysis to run
    ap.add_argument('--feature', '-f', type=int, required=True,
                    help='Which of the three features to run')
    
    # Optional parameter for analyses focusing on a specific user (i.e., contributor)
    ap.add_argument('--user', '-u', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific user')
    
    # Optional parameter for analyses focusing on a specific label
    ap.add_argument('--label', '-l', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific label')
    
    return ap.parse_args()



# Parse feature to call from command line arguments
args = parse_args()
# Add arguments to config so that they can be accessed in other parts of the application
config.overwrite_from_args(args)
    
# Run the feature specified in the --feature flag
if args.feature == 0:
    OverallAnalysis().run() #Analysis of labels
elif args.feature == 1:
    # Calling Feature1Analysis with optional filters if provided
    label = args.label or config.get_parameter('label')  
    user = args.user or config.get_parameter('creator')  
    
    # Initialize the DataLoader and load the DataFrame
    data_loader = DataLoader()
    df = data_loader.load_and_process_issues()  # This loads your issues data
    
    # Initialize the Analysis object
    analysis = Analysis()  
    
    # Filter the issues based on the provided label and creator
    filtered_df = analysis.filter_issues(df, label=label, creator=user)
    
    # Perform the analysis and visualization on the filtered issues
    analysis.analyze_and_visualize(filtered_df, df)
elif args.feature == 2:
    MonthIssueAnalysis().run() #Analysis of opened and closed tickets based on months
elif args.feature == 3:
    IssueCloseTimeAnalysis().run() #Analysis of average time it takes to close various issue types
else:
    print('Need to specify which feature to run with --feature flag.')
