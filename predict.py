import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def load_player_data(player_files):
    """Load and combine multiple season data for a player"""
    dfs = []
    for file in player_files:
        df = pd.read_csv(file)
        season = file.split('_')[-1].replace('.csv', '')
        df['season'] = season
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def calculate_season_stats(df, is_batsman=True):
    """Calculate season-wise statistics"""
    if is_batsman:
        season_stats = {
            'matches': len(df),
            'total_runs': df['total_runs'].sum(),
            'avg_runs': df['total_runs'].mean(),
            'total_balls': df['balls_played'].sum(),
            'strike_rate': (df['total_runs'].sum() / df['balls_played'].sum()) * 100 if df['balls_played'].sum() > 0 else 0,
            'fifties': len(df[df['total_runs'] >= 50]),
            'hundreds': len(df[df['total_runs'] >= 100]),
            'fours': df['fours'].sum(),
            'sixes': df['sixes'].sum(),
            'highest_score': df['total_runs'].max(),
            'ducks': len(df[df['total_runs'] == 0]),
            'not_outs': len(df[df['dismissed'] == False]),
            'avg_position': df['batting_position'].mean()
        }
    else:
        total_overs = df['balls_bowled'].sum() / 6
        season_stats = {
            'matches': len(df),
            'total_wickets': df['wickets_taken'].sum(),
            'avg_wickets': df['wickets_taken'].mean(),
            'economy_rate': df['runs_conceded'].sum() / total_overs if total_overs > 0 else 0,
            'total_overs': total_overs,
            'dot_balls': df['dot_balls'].sum(),
            'dot_ball_percentage': (df['dot_balls'].sum() / df['balls_bowled'].sum()) * 100 if df['balls_bowled'].sum() > 0 else 0,
            'best_figures': f"{df['wickets_taken'].max()}/{df.loc[df['wickets_taken'].idxmax(), 'runs_conceded']}",
            'three_wicket_hauls': len(df[df['wickets_taken'] >= 3]),
            'five_wicket_hauls': len(df[df['wickets_taken'] >= 5]),
            'avg_economy': df['bowling_economy'].mean()
        }
    return season_stats

def predict_season_performance(player_files, is_batsman=True, player_name=""):
    """Predict and analyze season-wise performance"""
    print(f"\nAnalyzing {player_name}'s Season-wise Performance")
    print("-" * 60)
    
    # Load and process data
    all_data = load_player_data(player_files)
    seasons = all_data['season'].unique()
    
    # Calculate and display season-wise stats
    print("\nSeason-wise Statistics:")
    print("-" * 40)
    
    season_stats_list = []
    for season in seasons:
        season_data = all_data[all_data['season'] == season]
        stats = calculate_season_stats(season_data, is_batsman)
        season_stats_list.append(stats)
        
        print(f"\nSeason {season}:")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"{key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Calculate career averages
    print("\nCareer Averages:")
    print("-" * 40)
    
    if is_batsman:
        career_stats = {
            'Average Runs': np.mean([stats['avg_runs'] for stats in season_stats_list]),
            'Career Strike Rate': np.mean([stats['strike_rate'] for stats in season_stats_list]),
            'Runs per Season': np.mean([stats['total_runs'] for stats in season_stats_list]),
            'Average Position': np.mean([stats['avg_position'] for stats in season_stats_list]),
            'Boundary Rate': np.mean([(stats['fours'] + stats['sixes'])/stats['matches'] for stats in season_stats_list])
        }
    else:
        career_stats = {
            'Average Wickets per Season': np.mean([stats['total_wickets'] for stats in season_stats_list]),
            'Career Economy Rate': np.mean([stats['economy_rate'] for stats in season_stats_list]),
            'Wickets per Match': np.mean([stats['avg_wickets'] for stats in season_stats_list]),
            'Average Dot Ball %': np.mean([stats['dot_ball_percentage'] for stats in season_stats_list])
        }
    
    for key, value in career_stats.items():
        print(f"{key}: {value:.2f}")
    
    # Predict next season's performance
    print("\nPredicted Performance for Next Season:")
    print("-" * 40)
    
    if is_batsman:
        # Use exponential weighted averages for prediction
        predicted_runs = np.average([stats['avg_runs'] for stats in season_stats_list], 
                                  weights=np.exp(range(len(season_stats_list))))
        predicted_runs = predicted_runs + 5
        predicted_sr = np.average([stats['strike_rate'] for stats in season_stats_list],
                                weights=np.exp(range(len(season_stats_list))))
        
        print(f"Predicted Average Runs: {predicted_runs:.2f}")
        print(f"Predicted Strike Rate: {predicted_sr:.2f}")
        
    else:
        predicted_wickets = np.average([stats['avg_wickets'] for stats in season_stats_list],
                                     weights=np.exp(range(len(season_stats_list))))
        predicted_wickets = predicted_wickets + 0.3
        predicted_economy = np.average([stats['economy_rate'] for stats in season_stats_list],
                                     weights=np.exp(range(len(season_stats_list))))
        
        print(f"Predicted Wickets per Match: {predicted_wickets:.2f}")
        print(f"Predicted Economy Rate: {predicted_economy:.2f}")

# Example usage
sp_narine_files = ['SP_Narine_IPL2017.csv', 'SP_Narine_IPL2018.csv', 'SP_Narine_IPL2024.csv']
ashutosh_sharma_files = ['Ashutosh_Sharma_IPL2024.csv']
rd_gaikwad_files = ['RD_Gaikwad_IPL2021.csv', 'RD_Gaikwad_IPL2022.csv', 'RD_Gaikwad_IPL2023.csv']
abishek_porel_files = ['Abishek_Porel_IPL2024.csv']
sa_yadav_files = ['SA_Yadav_IPL2021.csv', 'SA_Yadav_IPL2022.csv', 'SA_Yadav_IPL2023.csv', 'SA_Yadav_IPL2024.csv']
c_green_files = ['C_Green_IPL2023.csv', 'C_Green_IPL2024.csv']
sm_curran_files = ['SM_Curran_IPL2021.csv', 'SM_Curran_IPL2020.csv']
mohammad_nabi_files = ['Mohammad_Nabi_IPL2021.csv', 'Mohammad_Nabi_IPL2020.csv']
pp_chawla_files = ['PP_Chawla_IPL2023.csv', 'PP_Chawla_IPL2024.csv']
jj_bumrah_files = ['JJ_Bumrah_IPL2021.csv', 'JJ_Bumrah_IPL2022.csv', 'JJ_Bumrah_IPL2024.csv']
lh_ferguson_files = ['LH_Ferguson_IPL2022.csv', 'LH_Ferguson_IPL2023.csv', 'LH_Ferguson_IPL2024.csv']
g_coetzee_files = ['G_Coetzee_IPL2024.csv']

# Analyze players

#------------batsman---------------------
predict_season_performance(ashutosh_sharma_files, is_batsman=True, player_name="ashutosh_sharma_files")
predict_season_performance(rd_gaikwad_files, is_batsman=True, player_name="rd_gaikwad_files")
predict_season_performance(abishek_porel_files, is_batsman=True, player_name="abishek_porel_files")
predict_season_performance(sa_yadav_files, is_batsman=True, player_name="sa_yadav_files")
predict_season_performance(c_green_files, is_batsman=True, player_name="c_green_files")
predict_season_performance(sp_narine_files, is_batsman=True, player_name="sp_narine_files")
predict_season_performance(sm_curran_files, is_batsman=True, player_name="sm_curran_files")
predict_season_performance(mohammad_nabi_files, is_batsman=True, player_name="mohammad_nabi_files")


#---------------bowler--------------------------
predict_season_performance(g_coetzee_files, is_batsman=False, player_name="g_coetzee_files") 
predict_season_performance(lh_ferguson_files, is_batsman=False, player_name="lh_ferguson_files") 
predict_season_performance(jj_bumrah_files, is_batsman=False, player_name="jj_bumrah_files") 
predict_season_performance(pp_chawla_files, is_batsman=False, player_name="pp_chawla_files") 
predict_season_performance(mohammad_nabi_files, is_batsman=False, player_name="mohammad_nabi_files") 
predict_season_performance(sm_curran_files, is_batsman=False, player_name="sm_curran_files") 
predict_season_performance(c_green_files, is_batsman=False, player_name="c_green_files") 
predict_season_performance(sp_narine_files, is_batsman=False, player_name="sp_narine_files") 
