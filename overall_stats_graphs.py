import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Function to combine all CSV files into a single DataFrame
def combine_csv_files(csv_files):
    combined_df = pd.DataFrame()
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        # Extract player name from filename
        player_name = csv_file.split('_')[0]
        df['player_name'] = player_name  # Add player_name column
        combined_df = pd.concat([combined_df, df])
    return combined_df

# Function to create bowler dashboard
def create_bowler_dashboard(df, player_name):
    # Set style for better visualization
    plt.style.use('default')
    sns.set_theme()
    
    # Create figure and subplots
    fig = plt.figure(figsize=(15, 12))
    fig.suptitle(f"{player_name} Bowling Performance Analysis", fontsize=16, y=0.95)
    
    # 1. Economy
    ax1 = plt.subplot(2, 2, 1)
    sns.lineplot(data=df, x='serial_order', y='bowling_economy', color='orange', marker='o', ax=ax1)
    avg_economy = df['bowling_economy'].mean()
    ax1.axhline(y=avg_economy, color='gray', linestyle=':', label='Average Economy')
    ax1.text(0.5, avg_economy, f'Avg: {avg_economy:.2f}', color='gray', ha='center', va='bottom')
    ax1.set_title('Economy per Innings')
    ax1.set_xlabel('Match No')
    ax1.set_ylabel('Economy')
    ax1.legend()
    
    # 2. Total Wickets per Season
    ax2 = plt.subplot(2, 2, 2)
    sns.lineplot(data=df, x='serial_order', y='wickets_taken', color='green', marker='o', ax=ax2)
    avg_wickets = df['wickets_taken'].mean()
    ax2.axhline(y=avg_wickets, color='gray', linestyle=':', label='Average Wickets')
    ax2.text(0.5, avg_wickets, f'Avg: {avg_wickets:.2f}', color='gray', ha='center', va='bottom')
    ax2.set_title('Total Wickets per Season')
    ax2.set_xlabel('Match No')
    ax2.set_ylabel('Wickets')
    ax2.legend()
    
    # 3. Bowler's Strike Rate
    df['bowling_strike_rate'] = df['balls_bowled'] / df['wickets_taken']
    ax3 = plt.subplot(2, 2, 3)
    sns.lineplot(data=df, x='serial_order', y='bowling_strike_rate', color='blue', marker='o', ax=ax3)
    avg_strike_rate = df['bowling_strike_rate'].mean()
    ax3.axhline(y=avg_strike_rate, color='gray', linestyle=':', label='Average Strike Rate')
    ax3.text(0.5, avg_strike_rate, f'Avg: {avg_strike_rate:.2f}', color='gray', ha='center', va='bottom')
    ax3.set_title("Bowler's Strike Rate")
    ax3.set_xlabel('Match No')
    ax3.set_ylabel('Strike Rate')
    ax3.legend()
    
    # Adjust layout
    plt.tight_layout()
    
    # Ensure the "bowler" folder exists
    output_folder = "bowler"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Save the dashboard
    output_file = os.path.join(output_folder, f"{player_name}_bowler_dashboard.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_file

# Function to create batsman dashboard
def create_batsman_dashboard(df, player_name):
    # Set style for better visualization
    plt.style.use('default')
    sns.set_theme()
    
    # Create figure and subplots
    fig = plt.figure(figsize=(15, 12))
    fig.suptitle(f"{player_name} Batting Performance Analysis", fontsize=16, y=0.95)
    
    # 1. Total Runs
    ax1 = plt.subplot(2, 2, 1)
    sns.lineplot(data=df, x='serial_order', y='total_runs', color='orange', marker='o', ax=ax1)
    avg_runs = df['total_runs'].mean()
    ax1.axhline(y=avg_runs, color='gray', linestyle=':', label='Average Runs')
    ax1.text(0.5, avg_runs, f'Avg: {avg_runs:.2f}', color='gray', ha='center', va='bottom')
    ax1.set_title('Total Runs')
    ax1.set_xlabel('Match No')
    ax1.set_ylabel('Runs')
    ax1.legend()
    
    # 2. Batting Strike Rate
    ax2 = plt.subplot(2, 2, 2)
    sns.lineplot(data=df, x='serial_order', y='batting_strike_rate', color='green', marker='o', ax=ax2)
    avg_strike_rate = df['batting_strike_rate'].mean()
    ax2.axhline(y=avg_strike_rate, color='gray', linestyle=':', label='Average Strike Rate')
    ax2.text(0.5, avg_strike_rate, f'Avg: {avg_strike_rate:.2f}', color='gray', ha='center', va='bottom')
    ax2.set_title('Batting Strike Rate')
    ax2.set_xlabel('Match No')
    ax2.set_ylabel('Strike Rate')
    ax2.legend()
    
    # 3. Efficiency (No. of times crossed 30 for 1-4 batting position, 20 for 5 onwards)
    df['efficiency'] = df.apply(lambda row: 1 if (row['batting_position'] <= 4 and row['total_runs'] >= 30) or 
                                             (row['batting_position'] > 4 and row['total_runs'] >= 20) else 0, axis=1)
    ax3 = plt.subplot(2, 2, 3)
    sns.lineplot(data=df, x='serial_order', y='efficiency', color='blue', marker='o', ax=ax3)
    avg_efficiency = df['efficiency'].mean()
    ax3.axhline(y=avg_efficiency, color='gray', linestyle=':', label='Average Efficiency')
    ax3.text(0.5, avg_efficiency, f'Avg: {avg_efficiency:.2f}', color='gray', ha='center', va='bottom')
    ax3.set_title('Efficiency')
    ax3.set_xlabel('Match No')
    ax3.set_ylabel('Efficiency')
    ax3.legend()
    
    # Adjust layout
    plt.tight_layout()
    
    # Ensure the "batsman" folder exists
    output_folder = "batsman"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Save the dashboard
    output_file = os.path.join(output_folder, f"{player_name}_batsman_dashboard.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_file

# List your CSV files
csv_files = [
    "LH_Ferguson_IPL2023.csv",
    "LH_Ferguson_IPL2024.csv",
    "LH_Ferguson_IPL2021.csv",
    "LH_Ferguson_IPL2022.csv",
    "LH_Ferguson_IPL2020.csv",
    "LH_Ferguson_IPL2018.csv",
    "LH_Ferguson_IPL2017.csv"
]

combined_df = combine_csv_files(csv_files)

players = combined_df['player_name'].unique()
for player in players:
    player_df = combined_df[combined_df['player_name'] == player]
    player_df['serial_order'] = range(1, len(player_df) + 1)


try:
    # Create bowler dashboard
    if 'bowling_economy' in player_df.columns:
        bowler_dashboard_file = create_bowler_dashboard(player_df, player)
        print(f"Created bowler dashboard for {player}: {bowler_dashboard_file}")
    
    # Create batsman dashboard
    if 'total_runs' in player_df.columns:
        batsman_dashboard_file = create_batsman_dashboard(player_df, player)
        print(f"Created batsman dashboard for {player}: {batsman_dashboard_file}")
        
except Exception as e:
    print(f"Error processing {player}: {str(e)}")