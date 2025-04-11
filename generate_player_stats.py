import pandas as pd
input_filename = 'IPL2024.csv'  #Enter the CSV file of your choice to capture the player stats
deliveries = pd.read_csv(input_filename)

def player_exists(player_name):
    """Check if player exists in the dataset"""
    return (
        (deliveries['batter'] == player_name).any() or 
        (deliveries['bowler'] == player_name).any()
    )

def get_player_match_stats(player_name):
    # First check if player exists
    if not player_exists(player_name):
        print(f"Player '{player_name}' not found in the dataset.")
        return None
        
    # Get unique match IDs for the player
    player_matches = deliveries[
        (deliveries['batter'] == player_name) | 
        (deliveries['bowler'] == player_name)
    ]['match_id'].unique()
    
    match_stats_list = []
    
    for match_id in player_matches:
        # Filter data for specific match
        match_data = deliveries[deliveries['match_id'] == match_id]
        
        # Initialize match stats dictionary
        match_stats = {
            'match_id': match_id,
            'batting_team': '',
            'bowling_team': '',
            'opponent_team': '',
            'batting_position': 0,
            'total_runs': 0,
            'balls_played': 0,
            'balls_bowled': 0,
            'dot_balls': 0,
            'wickets_taken': 0,
            'dismissed': False,
            'dismissal_kind': None,
            'fours': 0,
            'sixes': 0,
            'batting_strike_rate': 0,
            'bowling_economy': 0,
            'runs_conceded': 0
        }
        
        # Batting statistics for the match
        batting_data = match_data[match_data['batter'] == player_name]
        if not batting_data.empty:
            match_stats['batting_team'] = batting_data['batting_team'].iloc[0]
            match_stats['opponent_team'] = batting_data['bowling_team'].iloc[0]
            
            # Calculate batting position
            innings_data = match_data[match_data['batting_team'] == match_stats['batting_team']]
            batters_before = innings_data[
                innings_data.index < batting_data.index.min()
            ]['batter'].unique()
            match_stats['batting_position'] = len(batters_before) + 1
            
            # Count only actual runs (excluding leg byes and byes)
            valid_runs = batting_data[
                ~batting_data['extras_type'].isin(['legbyes', 'byes'])
            ]
            match_stats['total_runs'] = valid_runs['batsman_runs'].sum()
            
            # Count legitimate balls faced (excluding wides and no balls)
            legitimate_balls = batting_data[
                ~batting_data['extras_type'].isin(['wides', 'noballs'])
            ]
            match_stats['balls_played'] = len(legitimate_balls)
            
            # Count fours and sixes
            match_stats['fours'] = len(valid_runs[valid_runs['batsman_runs'] == 4])
            match_stats['sixes'] = len(valid_runs[valid_runs['batsman_runs'] == 6])
            
            # Calculate batting strike rate
            if match_stats['balls_played'] > 0:
                match_stats['batting_strike_rate'] = round((match_stats['total_runs'] / match_stats['balls_played']) * 100, 2)
        
        # Bowling statistics for the match
        bowling_data = match_data[match_data['bowler'] == player_name]
        if not bowling_data.empty:
            match_stats['bowling_team'] = bowling_data['bowling_team'].iloc[0]
            if not match_stats['opponent_team']:  # Only set if not already set from batting
                match_stats['opponent_team'] = bowling_data['batting_team'].iloc[0]
            
            # Count only legitimate balls (excluding wides and no balls)
            legitimate_balls_bowled = bowling_data[
                ~bowling_data['extras_type'].isin(['wides', 'noballs'])
            ]
            match_stats['balls_bowled'] = len(legitimate_balls_bowled)
            
            # Count dot balls (no runs scored off the bat and no extras)
            dot_balls = bowling_data[
                (bowling_data['batsman_runs'] == 0) & 
                (bowling_data['extras_type'].isna()) &  # No extras
                (~bowling_data['extras_type'].isin(['wides', 'noballs']))  # Not a wide or no ball
            ]
            match_stats['dot_balls'] = len(dot_balls)
            
            # Count wickets (excluding run outs)
            wickets = bowling_data[
                (bowling_data['is_wicket'] == 1) & 
                (bowling_data['dismissal_kind'] != 'run out')
            ]
            match_stats['wickets_taken'] = len(wickets)
            
            # Calculate runs conceded (including extras but excluding byes and leg byes)
            runs_conceded = bowling_data[
                ~bowling_data['extras_type'].isin(['byes', 'legbyes'])
            ]['total_runs'].sum()
            match_stats['runs_conceded'] = runs_conceded
            
            # Calculate bowling economy
            overs_bowled = match_stats['balls_bowled'] / 6
            if overs_bowled > 0:
                match_stats['bowling_economy'] = round(match_stats['runs_conceded'] / overs_bowled, 2)
        
        # Check if player was dismissed in this match
        dismissal_data = match_data[match_data['player_dismissed'] == player_name]
        if not dismissal_data.empty:
            match_stats['dismissed'] = True
            match_stats['dismissal_kind'] = dismissal_data['dismissal_kind'].iloc[0]
        
        match_stats_list.append(match_stats)
    
    return match_stats_list

def generate_player_stats_csv(player_name):
    # Get the match statistics
    match_stats_list = get_player_match_stats(player_name)
    
    # If player doesn't exist, return None
    if match_stats_list is None:
        return None
        
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(match_stats_list)
    
    # Reorder columns to have match_id and opponent_team first
    columns_order = [
        'match_id',
        'opponent_team',
        'batting_team',
        'bowling_team',
        'batting_position',
        'total_runs',
        'balls_played',
        'balls_bowled',
        'dot_balls',
        'wickets_taken',
        'dismissed',
        'dismissal_kind',
        'fours',
        'sixes',
        'batting_strike_rate',
        'bowling_economy',
        'runs_conceded'
    ]
    df = df[columns_order]
    
    # Generate CSV filename
    base_input_filename = input_filename.replace('.csv', '')
    output_filename = f"{player_name.replace(' ', '_')}_{base_input_filename}.csv"
    
    df.to_csv(output_filename, index=False)
    print(f"Statistics saved to {output_filename}")
    
    return df

def process_player(player_name):
    """Process a single player with error handling"""
    print(f"\nProcessing statistics for {player_name}...")
    
    if not player_exists(player_name):
        print(f"Skipping {player_name} - Player not found in the dataset")
        return None
    
    stats_df = generate_player_stats_csv(player_name)
    if stats_df is not None:
        print(f"\nFirst few rows of statistics for {player_name}:")
        print(stats_df.head())
    return stats_df

# Example usage with multiple players
def main():
    player_names =players = [
    "SP Narine", 
    "RD Gaikwad", 
    "Abishek Porel",
    "SA Yadav",
    "C Green",
    "Ashutosh Sharma",
    "SM Curran",
    "Mohammad Nabi",
    "PP Chawla",
    "JJ Bumrah",
    "LH Ferguson",
    "G Coetzee"
    # continue with the list of players you want to get seasonal stats 
]
     # Add or modify player names as needed
    for player_name in player_names:
        process_player(player_name)

if __name__ == "__main__":
    main()