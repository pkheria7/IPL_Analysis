import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def combine_and_process_files(csv_files):
    """
    Combine all CSV files for a player into a single DataFrame.
    Add a 'season' column based on the last 4 digits of the filename.
    """
    # Initialize an empty list to store DataFrames from each file
    dataframes = []
    
    for csv_file in csv_files:
        # Read each CSV file
        df = pd.read_csv(csv_file)
        
        # Extract season (last 4 digits of the filename)
        season = csv_file.split('_')[-1].split('.')[0]  # Extract "YYYY" from "PlayerName_YYYY.csv"
        
        # Add a 'season' column to the DataFrame
        df['season'] = season
        
        # Append the DataFrame to the list
        dataframes.append(df)
    
    # Combine all DataFrames into one
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    return combined_df

def calculate_season_metrics(combined_df):
    """
    Calculate season-wise metrics from the combined DataFrame.
    """
    # Group by season and calculate metrics
    season_metrics = combined_df.groupby('season').agg(
        total_wickets=('wickets_taken', 'sum'),
        total_balls_bowled=('balls_bowled', 'sum'),
        total_runs_conceded=('runs_conceded', 'sum')
    ).reset_index()
    
    # Calculate derived metrics
    season_metrics['runs_per_wicket'] = season_metrics['total_runs_conceded'] / season_metrics['total_wickets']
    season_metrics['balls_per_wicket'] = season_metrics['total_balls_bowled'] / season_metrics['total_wickets']
    season_metrics['economy_rate'] = season_metrics['total_runs_conceded'] * 6 / season_metrics['total_balls_bowled']
    
    # Handle potential division-by-zero issues
    season_metrics['runs_per_wicket'] = season_metrics['runs_per_wicket'].fillna(0)
    season_metrics['balls_per_wicket'] = season_metrics['balls_per_wicket'].fillna(0)
    
    return season_metrics

def create_combined_dashboard(season_metrics, player_name):
    """
    Create a combined dashboard with four graphs based on season-wise metrics.
    """
    # Set style for better visualization
    sns.set_theme(style="whitegrid")
    plt.style.use('default')
    
    # Create figure and subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f"{player_name} Season-wise Performance Analysis", fontsize=16, y=0.95)
    
    # 1. Total wickets taken per season
    sns.barplot(data=season_metrics, x='season', y='total_wickets', color='orange', ax=axes[0, 0])
    axes[0, 0].set_title('Total Wickets per Season')
    axes[0, 0].set_xlabel('Season')
    axes[0, 0].set_ylabel('Wickets')
    
    # 2. Runs per wicket
    sns.lineplot(data=season_metrics, x='season', y='runs_per_wicket', marker='o', color='green', ax=axes[0, 1])
    axes[0, 1].set_title('Average')
    axes[0, 1].set_xlabel('Season')
    axes[0, 1].set_ylabel('Runs/Wicket')
    
    # 3. Balls per wicket
    sns.lineplot(data=season_metrics, x='season', y='balls_per_wicket', marker='o', color='blue', ax=axes[1, 0])
    axes[1, 0].set_title('Strike Rate')
    axes[1, 0].set_xlabel('Season')
    axes[1, 0].set_ylabel('Balls/Wicket')
    
    # 4. Economy rate per season
    sns.barplot(data=season_metrics, x='season', y='economy_rate', color='red', ax=axes[1, 1])
    axes[1, 1].set_title('Economy Rate per Season')
    axes[1, 1].set_xlabel('Season')
    axes[1, 1].set_ylabel('Economy Rate')
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Ensure the "output" folder exists
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Save the dashboard as a PNG file
    output_file = os.path.join(output_folder, f"{player_name}_combined_dashboard.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_file

def main():
    # List of CSV files for the player
    csv_files = [
    "SP_Narine_IPL2012.csv",
    "SP_Narine_IPL2013.csv",
    "SP_Narine_IPL2014.csv",
    "SP_Narine_IPL2015.csv",
    "SP_Narine_IPL2016.csv",
    "SP_Narine_IPL2017.csv",
    "SP_Narine_IPL2018.csv",
    "SP_Narine_IPL2019.csv",
    "SP_Narine_IPL2020.csv",
    "SP_Narine_IPL2021.csv",
    "SP_Narine_IPL2022.csv",
    "SP_Narine_IPL2023.csv",
    "SP_Narine_IPL2024.csv"
]
    
    # Combine all CSV files into a single DataFrame
    combined_df = combine_and_process_files(csv_files)
    
    # Extract player name from the first file
    player_name = csv_files[0].split('_')[0]
    
    # Calculate season-wise metrics
    season_metrics = calculate_season_metrics(combined_df)
    
    # Debugging: Print the season metrics to verify the data
    print("Season Metrics:")
    print(season_metrics)
    
    # Create the combined dashboard
    dashboard_file = create_combined_dashboard(season_metrics, player_name)
    
    print(f"Dashboard created: {dashboard_file}")

# Run the script
if __name__ == "__main__":
    main()