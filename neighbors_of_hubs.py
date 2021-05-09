import csv

BETA_CSV = 'data/out/intl_arrivals_by_airport.csv'
STATES_ABBREV_CSV = 'data/in/states_abbreviations.csv'
FLIGHTS_CSV = 'data/in/domestic_flights.csv'

NEIGHBORS_HUBS_CSV_OUT = 'data/out/neighbors_hubs.csv'

def get_states_abbreviations_from_csv():
    abbreviations_to_states = dict()
    with open(STATES_ABBREV_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            abbreviations_to_states[row['STATE_ABBREVIATION']] = row['STATE']
    return abbreviations_to_states

def get_beta_dict_from_csv():
    beta_dict = dict()
    with open(BETA_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            beta_dict[row['AIRPORT']] = float(row['BETA_ITALY'])
    return beta_dict


def compute_neighbors_of_hubs(states_abbreviations, beta_italy):
    state_totals = dict()
    for state in states_abbreviations.keys():
        state_totals[state] = 0

    with open(FLIGHTS_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dest_state = row['DEST_STATE']
            origin_city = row['ORIGIN_CITY']
            if dest_state in states_abbreviations.keys() and origin_city in beta_italy.keys():
                state_totals[dest_state] += beta_italy[origin_city] * float(row['PASSENGERS'])

    return state_totals


def write_output(states_abbreviations, state_totals):
    max_total_italy = max(state_totals.values())

    with open(NEIGHBORS_HUBS_CSV_OUT, 'w') as csvfile:
        fieldnames = ['STATE', 'STATE_ABBREVIATION', 'NEIGHBORS_HUBS_ITALY']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for state in states_abbreviations.keys():
            neighbor_italy = state_totals[state]
            neighbor_italy_scaled = (1.0 * neighbor_italy) / max_total_italy
            writer.writerow({'STATE': states_abbreviations[state],
                            'STATE_ABBREVIATION': state,
                            'NEIGHBORS_HUBS_ITALY': neighbor_italy_scaled})



def neighbors_of_hubs_main():
    states_abbreviations = get_states_abbreviations_from_csv()
    beta_italy = get_beta_dict_from_csv()

    state_totals = compute_neighbors_of_hubs(states_abbreviations, beta_italy)

    write_output(states_abbreviations, state_totals)
