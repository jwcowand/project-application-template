

"""
Starting point of the application. This module is invoked from
the command line to run the analyses.
"""

import argparse

import config
from example_analysis import ExampleAnalysis
from month_issue_analysis import MonthIssueAnalysis

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
    ExampleAnalysis().run() #Analysis of labels
elif args.feature == 1:
    pass #Analysis of top closing users 
elif args.feature == 2:
    MonthIssueAnalysis().run() #Analysis of opened and closed tickets based on months
elif args.feature == 3:
    pass #Analysis of average time it takes to close various issue types
else:
    print('Need to specify which feature to run with --feature flag.')
