import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os  # Import os module to handle file paths

def create_bowler_dashboard(csv_file, player_name):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Add a new column 'serial_order' to replace 'match_id'
    df['serial_order'] = range(1, len(df) + 1)
    
    # Set style for better visualization
    plt.style.use('default')  # Changed from 'seaborn' to 'default'
    sns.set_theme()  # This will apply seaborn styling
    
    # Create figure and subplots
    fig = plt.figure(figsize=(15, 12))
    fig.suptitle(f"{player_name} Performance Analysis", fontsize=16, y=0.95)
    
    # 1. Economy: bowling_economy vs match_id
    ax1 = plt.subplot(2, 2, 1)
    sns.lineplot(data=df, x='serial_order', y='bowling_economy', color='orange', marker='o', ax=ax1)
    avg_economy = df['bowling_economy'].mean()
    ax1.axhline(y=avg_economy, color='gray', linestyle=':', label='Average Economy')
    ax1.text(0.5, avg_economy, f'Avg: {avg_economy:.2f}', color='gray', ha='center', va='bottom')
    ax1.set_title('Economy per Innings')
    ax1.set_xlabel('Match No')
    ax1.set_ylabel('Economy')
    ax1.legend()
    
    # 2. Wickets per innings: wickets_taken vs match_id
    ax2 = plt.subplot(2, 2, 2)
    sns.lineplot(data=df, x='serial_order', y='wickets_taken', color='green', marker='o', ax=ax2)
    avg_wickets = df['wickets_taken'].mean()
    ax2.axhline(y=avg_wickets, color='gray', linestyle=':', label='Average Wickets')
    ax2.text(0.5, avg_wickets, f'Avg: {avg_wickets:.2f}', color='gray', ha='center', va='bottom')
    ax2.set_title('Wickets per Innings')
    ax2.set_xlabel('Match No')
    ax2.set_ylabel('Wickets')
    ax2.legend()
    
    # 3. Dot balls % = dot_balls * 100 / balls_bowled
    df['dot_balls_percentage'] = (df['dot_balls'] * 100 / df['balls_bowled']).fillna(0)
    ax3 = plt.subplot(2, 2, 3)
    sns.lineplot(data=df, x='serial_order', y='dot_balls_percentage', color='blue', marker='o', ax=ax3)
    avg_dot_balls_percentage = df['dot_balls_percentage'].mean()
    ax3.axhline(y=avg_dot_balls_percentage, color='gray', linestyle=':', label='Average Dot Balls %')
    ax3.text(0.5, avg_dot_balls_percentage, f'Avg: {avg_dot_balls_percentage:.2f}%', color='gray', ha='center', va='bottom')
    ax3.set_title('Dot Balls Percentage')
    ax3.set_xlabel('Match No')
    ax3.set_ylabel('Dot Balls %')
    ax3.legend()
    
    # 4. Balls bowled (inning wise) = balls_bowled vs match_id
    ax4 = plt.subplot(2, 2, 4)
    sns.lineplot(data=df, x='serial_order', y='balls_bowled', color='red', marker='o', ax=ax4)
    avg_balls_bowled = df['balls_bowled'].mean()
    ax4.axhline(y=avg_balls_bowled, color='gray', linestyle=':', label='Average Balls Bowled')
    ax4.text(0.5, avg_balls_bowled, f'Avg: {avg_balls_bowled:.2f}', color='gray', ha='center', va='bottom')
    ax4.set_title('Balls Bowled per Innings')
    ax4.set_xlabel('Match No')
    ax4.set_ylabel('Balls Bowled')
    ax4.legend()
    
    # Adjust layout
    plt.tight_layout()
    
    # Ensure the "bowler" folder exists
    output_folder = "bowler"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Save the dashboard with the same name as the input file but with a .png extension in the "bowler" folder
    output_file = os.path.join(output_folder, csv_file.replace('.csv', '_dashboard.png'))
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_file

def process_multiple_files(csv_files):
    for csv_file in csv_files:
        # Extract player name and year from filename
        player_name = csv_file.split('_')[0]  # Assuming filename format: "PlayerName_Year.csv"
        year = csv_file.split('_')[1].split('.')[0]  # Extract the year part
        player_surname = player_name.split(' ')[-1]  # Extract the surname
        full_title = f"{player_surname} {year}"
        
        try:
            # Create matplotlib dashboard
            dashboard_file = create_bowler_dashboard(csv_file, full_title)
            print(f"Created dashboard for {full_title}: {dashboard_file}")
            
        except Exception as e:
            print(f"Error processing {csv_file}: {str(e)}")

# List your CSV files
csv_files =[
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

# Process all files
if __name__ == "__main__":
    process_multiple_files(csv_files)