import json
import pandas as pd

class DataLoader:
    def __init__(self, config_path='config.json'):
        self.file_path = self.get_file_path(config_path)

    # Load the file path from config.json
    def get_file_path(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config['file_path']

    # Load the issues from the JSON file
    def load_issues(self):
        with open(self.file_path, 'r') as f:
            issues = json.load(f)
        return issues

    # Helper function to find who closed the issue and when
    def get_closing_event(self, events):
        for event in events:
            if event.get("event_type") == "closed":
                return event.get("author"), event.get("event_date")
        return None, None
    
    # Process the issues and return them as a pandas DataFrame
    def process_issues(self, issues):
        processed_issues = []
        for issue in issues:
            # Extract the closed event author and date if the state is closed
            closed_by, closed_at = None, None
            if issue.get('state') == 'closed':
                closed_by, closed_at = self.get_closing_event(issue.get("events", []))
            
            processed_issue = {
                'number': issue.get('number'),
                'creator': issue.get('creator'),
                'title': issue.get('title'),
                'state': issue.get('state'),
                'created_at': issue.get('created_date'),
                'updated_at': issue.get('updated_date'),
                'labels': issue.get('labels', []),
                'closed_by': closed_by,          # Add closed_by column
                'closed_at': closed_at           # Add closed_at column
            }
            processed_issues.append(processed_issue)
        
        # Convert to DataFrame for better visualization
        df = pd.DataFrame(processed_issues)
        
        # Data cleaning
        if not df.empty:
            df = df[df['number'].notnull()]
            df = df.drop_duplicates(subset='number')
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            df['updated_at'] = pd.to_datetime(df['updated_at'], errors='coerce')
            df['closed_at'] = pd.to_datetime(df['closed_at'], errors='coerce')
            df['closed_by'] = df['closed_by'].str.strip().str.lower()
            df['labels'] = df['labels'].apply(lambda x: x if isinstance(x, list) else [])
            df['title'] = df['title'].str.strip().str.lower()
            df['state'] = df['state'].str.strip().str.lower()
        else:
            print("Empty DataFrame after processing.")
        
        return df

    def load_and_process_issues(self):
        # Load and process issues
        issues = self.load_issues()
        
        # Check if issues were loaded correctly
        if not issues:
            print("No issues found in the JSON file.")
            return pd.DataFrame()  # Return an empty DataFrame if no issues found
        
        # Process the issues and return the DataFrame
        processed_df = self.process_issues(issues)
        return processed_df

# Example of how to use the DataLoader class
if __name__ == '__main__':
    data_loader = DataLoader()
    df = data_loader.load_and_process_issues()

    # Display basic information about the DataFrame
    if not df.empty:
        null_counts = df.isnull().sum()
        print(null_counts)
        print(df.head())
        print(df.describe())
        print(df.info())
        print(df.columns)
