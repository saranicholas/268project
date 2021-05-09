import csv
from decimal import Decimal


CITY_RANKS_CSV = 'data/out/airport_pageranks.csv'
STATES_ABBREV_CSV = 'data/in/states_abbreviations.csv'

STATE_RANKS_CSV_OUT = 'data/out/state_pageranks.csv'


def get_states_abbreviations_from_csv():
    abbreviations_to_states = dict()
    with open(STATES_ABBREV_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            abbreviations_to_states[row['STATE_ABBREVIATION']] = row['STATE']
    return abbreviations_to_states

def compute_state_ranks(rank_type):
    state_ranks = dict()
    with open(CITY_RANKS_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            airport = row['AIRPORT']
            state = airport[airport.index(",")+2 : ]
            if state in state_ranks.keys():
                state_ranks[state] += Decimal(row[rank_type])
            else:
                state_ranks[state] = Decimal(row[rank_type])
    return state_ranks

def write_output(states_abbreviations, state_ranks_normalized, state_ranks_china, state_ranks_italy, state_ranks_combined):
    with open(STATE_RANKS_CSV_OUT, 'w') as csvfile:
        fieldnames = ['STATE', 'STATE_ABBREVIATION', 'RANK_NORMALIZED', 'RANK_CHINA', 'RANK_ITALY', 'RANK_COMBINED']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        max_normalized = max(state_ranks_normalized.values())
        max_china = max(state_ranks_normalized.values())
        max_italy = max(state_ranks_italy.values())
        max_combined = max(state_ranks_combined.values())
        for state in states_abbreviations.keys():
            rank_normalized = state_ranks_normalized[state] if state in state_ranks_normalized.keys() else 0
            rank_china = state_ranks_china[state] if state in state_ranks_china.keys() else 0
            rank_italy = state_ranks_italy[state] if state in state_ranks_italy.keys() else 0
            rank_combined = state_ranks_combined[state] if state in state_ranks_combined.keys() else 0
            writer.writerow({'STATE': states_abbreviations[state],
                            'STATE_ABBREVIATION': state,
                            'RANK_NORMALIZED': rank_normalized,
                            'RANK_CHINA': rank_china,
                            'RANK_ITALY': rank_italy,
                            'RANK_COMBINED': rank_combined})




def state_pageranks_main():
    print("Computing state page ranks...")
    states_abbreviations = get_states_abbreviations_from_csv()
    state_ranks_normalized = compute_state_ranks('RANK_NORMALIZED')
    state_ranks_china = compute_state_ranks('RANK_CHINA')
    state_ranks_italy = compute_state_ranks('RANK_ITALY')
    state_ranks_combined = compute_state_ranks('RANK_COMBINED')

    write_output(states_abbreviations, state_ranks_normalized, state_ranks_china, state_ranks_italy, state_ranks_combined)
    print("State page rank computation complete")
