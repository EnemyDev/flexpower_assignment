import pandas as pd
import numpy as np
from datetime import datetime
from itertools import product

def prepare_data(df):
    # Convert time to datetime for grouping
    df['Datetime'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M')
    
    # Use 'IntradayPricePriceQuarterHourlyEURMWh' for quarter-hourly analysis
    df['PriceChange'] = df['IntradayPricePriceQuarterHourlyEURMWh'].diff()
    
    # Define states
    def state(x):
        if x > 0: return 'B'  # Bullish
        elif x < 0: return 'S'  # Bearish
        else: return 'N'  # Neutral (assuming no change or very small change is neutral)
    
    df['State'] = df['PriceChange'].apply(state)
    
    return df

def create_transition_matrix(df):
    states = ['B', 'S', 'N']
    # Transition count
    transition_counts = {s: {s2: 0 for s2 in states} for s in states}
    
    for i in range(len(df) - 1):
        current_state = df['State'].iloc[i]
        next_state = df['State'].iloc[i + 1]
        transition_counts[current_state][next_state] += 1

    # Convert to transition matrix (probabilities)
    transition_matrix = pd.DataFrame(transition_counts).T
    transition_probs = transition_matrix.to_numpy() / transition_matrix.sum(axis=1).to_numpy()[:, np.newaxis]
    
    # Convert back to DataFrame with proper indices and columns
    transition_matrix = pd.DataFrame(transition_probs, index=transition_matrix.index, columns=transition_matrix.columns)
    
    return transition_matrix

def get_probability_of_sequence(transition_matrix, sequence):
    probability = 1.0
    for i in range(len(sequence) - 1):
        probability *= transition_matrix.loc[sequence[i], sequence[i + 1]]
    return probability * 100  # Convert to percentage

# Load the CSV file with correct date format parsing
df = pd.read_csv('cleaned.csv', 
                 parse_dates=['time'], 
                 date_format='%m/%d/%y %H:%M')

# Prepare data
df = prepare_data(df)

# Create transition matrix
transition_matrix = create_transition_matrix(df)

# Print transition matrix for inspection
# print("Transition Matrix:\n", transition_matrix.to_string())

# Print probabilities
for state in transition_matrix.index:
    print(f"\nProbabilities for transitions from {state}:")
    for next_state, prob in zip(transition_matrix.columns, transition_matrix.loc[state]):
        print(f"  {state} -> {next_state}: {prob*100:.2f}%")

# Generate all possible 4-quarter sequences
states = ['B', 'S', 'N']
all_sequences = [''.join(seq) for seq in product(states, repeat=4)]

# Filter sequences by starting state and calculate probabilities
bullish_sequences = [seq for seq in all_sequences if seq[0] == 'B']
bearish_sequences = [seq for seq in all_sequences if seq[0] == 'S']

print("\nAll 4-Quarter Sequences Starting from Bullish:")
bullish_probs = []
for seq in bullish_sequences:
    prob = get_probability_of_sequence(transition_matrix, seq)
    print(f"{seq}: {prob:.2f}%")
    bullish_probs.append(prob)

print("\nAll 4-Quarter Sequences Starting from Bearish:")
bearish_probs = []
for seq in bearish_sequences:
    prob = get_probability_of_sequence(transition_matrix, seq)
    print(f"{seq}: {prob:.2f}%")
    bearish_probs.append(prob)

# Mathematical test of validity
def check_validity(probs):
    total = sum(probs)
    print(f"\nSum of probabilities: {total:.2f}%")
    if abs(total - 100) < 0.01:  # Tolerance for floating-point imprecision
        print("The sum of probabilities is valid (approximately 100%).")
    else:
        print("Warning: The sum of probabilities deviates from 100%.")

# Check validity for both sets of probabilities
print("\nChecking Bullish Sequences:")
check_validity(bullish_probs)
print("\nChecking Bearish Sequences:")
check_validity(bearish_probs)

# Find the best strategy for the last (4th) quarter
def find_best_last_quarter_strategy(sequences, transition_matrix):
    best_strategies = {}
    for start_state in ['B', 'S']:
        filtered_sequences = [seq for seq in sequences if seq[0] == start_state]
        
        best_prob = 0
        best_seq = None
        for seq in filtered_sequences:
            # Only look at the last quarter
            last_quarter = seq[-1]
            prob = transition_matrix.loc[seq[-2], last_quarter] * 100  # Probability of last transition
            if prob > best_prob:
                best_prob = prob
                best_seq = last_quarter
        
        best_strategies[start_state] = (best_seq, best_prob)
    
    return best_strategies

# Calculate best strategies for last quarter
# best_strategies_last_quarter = find_best_last_quarter_strategy(all_sequences, transition_matrix)

# Output best strategies for last quarter
# for start_state, (seq, prob) in best_strategies_last_quarter.items():
#     print(f"\nBest strategy for the last quarter from {start_state}: {seq} with probability {prob:.2f}%")