import csv

STATES_ABBREV_CSV = 'data/in/states_abbreviations.csv'

INTL_ARRIVALS_CSV = 'data/out/intl_arrivals_by_state.csv'
NEIGHBORS_HUBS_CSV = 'data/out/neighbors_hubs.csv'
STATE_PAGERANKS_CSV = 'data/out/state_pageranks.csv'

CASES_CSV = 'data/out/state_cases.csv'

REGRESSION_CSV = 'data/regression/regression_data.csv'


def get_states_abbreviations_from_csv():
    abbreviations_to_states = dict()
    with open(STATES_ABBREV_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            abbreviations_to_states[row['STATE_ABBREVIATION']] = row['STATE']
    return abbreviations_to_states

def get_dict_from_csv(CSV_IN, category):
    csv_dict = dict()
    with open(CSV_IN, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_dict[row['STATE_ABBREVIATION']] = row[category]
    return csv_dict


def write_output(states_abbreviations, passengers_from_italy, neighbors_hubs, pageranks_normalized, pageranks_italy):
    with open(REGRESSION_CSV, 'w') as csvfile:
        fieldnames = ['STATE', 'STATE_ABBREVIATION', 'PASSENGERS_FROM_ITALY_SCALED', 'NEIGHBORS_HUBS_ITALY', 'RANK_NORMALIZED', 'RANK_ITALY']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for state in states_abbreviations.keys():
            from_italy = passengers_from_italy[state] if state in passengers_from_italy.keys() else 0
            neighbor = neighbors_hubs[state] if state in neighbors_hubs.keys() else 0
            rank_normalized = pageranks_normalized[state] if state in pageranks_normalized.keys() else 0
            rank_italy = pageranks_italy[state] if state in pageranks_italy else 0
            writer.writerow({'STATE': states_abbreviations[state],
                            'STATE_ABBREVIATION': state,
                            'PASSENGERS_FROM_ITALY_SCALED': from_italy,
                            'NEIGHBORS_HUBS_ITALY': neighbor,
                            'RANK_NORMALIZED': rank_normalized,
                            'RANK_ITALY': rank_italy})

def format_regression_data_main():
    states_abbreviations = get_states_abbreviations_from_csv()
    passengers_from_italy = get_dict_from_csv(INTL_ARRIVALS_CSV, 'PASSENGERS_FROM_ITALY_SCALED')
    neighbors_hubs = get_dict_from_csv(NEIGHBORS_HUBS_CSV, 'NEIGHBORS_HUBS_ITALY')
    pageranks_normalized = get_dict_from_csv(STATE_PAGERANKS_CSV, 'RANK_NORMALIZED')
    pageranks_italy = get_dict_from_csv(STATE_PAGERANKS_CSV, 'RANK_ITALY')

    write_output(states_abbreviations, passengers_from_italy, neighbors_hubs, pageranks_normalized, pageranks_italy)
