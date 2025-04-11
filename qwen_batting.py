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
    Calculate season-wise metrics for a batsman.
    """
    # Group by season and calculate metrics
    season_metrics = combined_df.groupby('season').agg(
        total_runs=('total_runs', 'sum'),
        total_balls_played=('balls_played', 'sum'),
        total_dismissals=('dismissed', lambda x: x.sum()),  # Count dismissals where dismissed == True
        matches_played=('match_id', 'nunique')  # Count unique matches played
    ).reset_index()
    
    # Calculate derived metrics
    season_metrics['runs_per_dismissal'] = season_metrics['total_runs'] / season_metrics['total_dismissals']
    season_metrics['runs_per_ball'] = (season_metrics['total_runs'] / season_metrics['total_balls_played']) * 100  # Runs per 100 balls
    
    # Calculate percentage of times strike rate > 140 when balls played > 0
    def high_strike_rate_percentage(df):
        valid_matches = df[df['balls_played'] > 0]
        high_strike_rate = valid_matches[valid_matches['batting_strike_rate'] > 140]
        return len(high_strike_rate) / len(valid_matches) * 100 if len(valid_matches) > 0 else 0
    
    season_metrics['high_strike_rate_percentage'] = combined_df.groupby('season').apply(high_strike_rate_percentage).values
    
    # Handle potential division-by-zero issues
    season_metrics['runs_per_dismissal'] = season_metrics['runs_per_dismissal'].fillna(0)
    season_metrics['runs_per_ball'] = season_metrics['runs_per_ball'].fillna(0)
    
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
    
    # 1. Total runs per season
    sns.barplot(data=season_metrics, x='season', y='total_runs', color='orange', ax=axes[0, 0])
    axes[0, 0].set_title('Total Runs per Season')
    axes[0, 0].set_xlabel('Season')
    axes[0, 0].set_ylabel('Runs')
    
    # 2. Runs per dismissal
    sns.lineplot(data=season_metrics, x='season', y='runs_per_dismissal', marker='o', color='green', ax=axes[0, 1])
    axes[0, 1].set_title('Runs per Dismissal')
    axes[0, 1].set_xlabel('Season')
    axes[0, 1].set_ylabel('Runs/Dismissal')
    
    # 3. Runs per 100 balls
    sns.lineplot(data=season_metrics, x='season', y='runs_per_ball', marker='o', color='blue', ax=axes[1, 0])
    axes[1, 0].set_title('Strike Rate')
    axes[1, 0].set_xlabel('Season')
    axes[1, 0].set_ylabel('Runs/100 Balls')
    
    # 4. Percentage of times strike rate > 140 when balls played > 0
    sns.barplot(data=season_metrics, x='season', y='high_strike_rate_percentage', color='red', ax=axes[1, 1])
    axes[1, 1].set_title('Percentage of High Strike Rate (> 140)')
    axes[1, 1].set_xlabel('Season')
    axes[1, 1].set_ylabel('Percentage (%)')
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Ensure the "output" folder exists
    output_folder = "output_batsmen"
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
    "C_Green_IPL2023.csv",
    "C_Green_IPL2024.csv"
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