# Player Performance Analysis Dashboard

## Overview
This project analyzes cricket player performance using historical match data. It generates visual dashboards for both batsmen and bowlers, providing insights into their performance metrics over multiple seasons.

## Features
- Visualizations for runs scored, strike rates, boundary percentages, and batting positions for batsmen.
- Metrics for wickets taken, economy rates, and dot balls for bowlers.
- Predictive modeling for future performance based on historical data.

## Data Files
The project uses CSV files containing player performance data. The expected format for the CSV files is as follows:

- **Batsman Data**: 
  - `SA_Yadav_IPL2021.csv`
  - `SA_Yadav_IPL2022.csv`
  - (Add more files as needed)

- **Bowler Data**: 
  - `JJ_Bumrah_IPL2021.csv`
  - `JJ_Bumrah_IPL2022.csv`
  - (Add more files as needed)

### Data Structure
Each CSV file should contain the following columns:
- `match_id`: Unique identifier for each match
- `opponent_team`: Name of the opposing team
- `batting_team`: Name of the team the player batted for
- `bowling_team`: Name of the team the player bowled for
- `batting_position`: Position in the batting order
- `total_runs`: Runs scored by the batsman
- `balls_played`: Balls faced by the batsman
- `balls_bowled`: Balls bowled by the bowler
- `dot_balls`: Number of dot balls bowled
- `wickets_taken`: Wickets taken by the bowler
- `dismissed`: Whether the batsman was dismissed
- `dismissal_kind`: Type of dismissal (e.g., caught, bowled)
- `fours`: Number of fours hit
- `sixes`: Number of sixes hit
- `batting_strike_rate`: Strike rate of the batsman
- `bowling_economy`: Economy rate of the bowler
- `runs_conceded`: Runs conceded by the bowler

## Working Directories
- **Data Directory**: Place all CSV files in the same directory as the script or update the paths in the code accordingly.
- **Output Directory**: The script will create an `output_hyper_files` directory to store generated Tableau Hyper files and dashboards.

## Requirements
To run this project, you need the following Python packages:

- pandas
- matplotlib
- seaborn
- scikit-learn

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## requirements.txt
Create a `requirements.txt` file with the following content:
