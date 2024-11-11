# ENPM611 Project Group 2
This project contains a set of analysis that can be run against issues from the Poetry repo. These analysis were made to help contributors to poetry understand and visualize various statistics of issues.


### Install dependencies

In the root directory of the application, create a virtual environment, activate that environment, and install the dependencies like so:

```
pip install -r requirements.txt
```

### Download and configure the data file

Ensure you have a json data file of the poetry issues on github. Update the `config.json` with the path to the file.


### Run an analysis

With everything set up, you should be able to run various analysis.

Analysis One:
Analysis of most common labels from issues in poetry.
```
python run.py --feature 0
```

Analysis Two:
Analysis of most closed issues by user and labels. Can pass user or label arguments.
```
python run.py --feature 1 --user radoering
```
Analysis Three:
Analysis of monthly closed and opened issues.
```
python run.py --feature 2
```
Analysis Four:
Analysis of average time it takes to close various types of issues.
```
python run.py --feature 3
```

