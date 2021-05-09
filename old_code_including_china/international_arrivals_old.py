import csv
import numpy as np
from decimal import Decimal

AIRPORTS_CSV = 'data/in/airports.csv'

FROM_CHINA_CSV = 'data/in/flights_from_china.csv'
FROM_ITALY_CSV = 'data/in/flights_from_italy.csv'
STATES_ABBREV_CSV = 'data/in/states_abbreviations.csv'

AIRPORTS_CSV_OUT = 'data/out/intl_arrivals_by_airport.csv'
STATES_CSV_OUT = 'data/out/intl_arrivals_by_state.csv'


def get_airports_from_csv():
    airports = []
    with open(AIRPORTS_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            airports.append(row['AIRPORT'])
    return airports


def get_states_abbreviations_from_csv():
    abbreviations_to_states = dict()
    with open(STATES_ABBREV_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            abbreviations_to_states[row['STATE_ABBREVIATION']] = row['STATE']
    return abbreviations_to_states


def get_count_by_category(arrivals_csv, category):
    count = dict()
    with open(arrivals_csv, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row[category] in count.keys():
                count[row[category]] += int(row['PASSENGERS'])
            else:
                count[row[category]] = int(row['PASSENGERS'])
    return count


def get_combined_count(category, count_china, count_italy):
    count_combined = dict()
    for item in category:
        from_china = count_china[item] if item in count_china.keys() else 0
        from_italy = count_italy[item] if item in count_italy.keys() else 0
        combined = from_china + from_italy
        count_combined[item] = combined
    return count_combined


def write_output_states(states_abbreviations, states_count_china, states_count_italy, states_count_combined):
    with open(STATES_CSV_OUT, 'w') as csvfile:
        fieldnames = ['STATE', 'STATE_ABBREVIATION', 'PASSENGERS_FROM_CHINA', 'PASSENGERS_FROM_ITALY', 'PASSENGERS_COMBINED']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for state in states_abbreviations.keys():
            from_china = states_count_china[state] if state in states_count_china.keys() else 0
            from_italy = states_count_italy[state] if state in states_count_italy.keys() else 0
            combined = states_count_combined[state] if state in states_count_combined.keys() else 0
            writer.writerow({'STATE': states_abbreviations[state],
                            'STATE_ABBREVIATION': state,
                            'PASSENGERS_FROM_CHINA': from_china,
                            'PASSENGERS_FROM_ITALY': from_italy,
                            'PASSENGERS_COMBINED': combined})


def write_output_airports(airports, airports_count_china, airports_count_italy, airports_count_combined, max_china, max_italy, max_combined):
    with open(AIRPORTS_CSV_OUT, 'w') as csvfile:
        fieldnames = ['AIRPORT', 'PASSENGERS_FROM_CHINA', 'PASSENGERS_FROM_ITALY', 'PASSENGERS_COMBINED', 'BETA_CHINA', 'BETA_ITALY', 'BETA_COMBINED', 'BETA_NORMALIZED']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ap in airports:
            from_china = airports_count_china[ap] if ap in airports_count_china.keys() else 0
            from_italy = airports_count_italy[ap] if ap in airports_count_italy.keys() else 0
            combined = airports_count_combined[ap] if ap in airports_count_combined.keys() else 0
            beta_china = (1.0 * from_china) / max_china
            beta_italy = (1.0 * from_italy) / max_italy
            beta_combined = (1.0 * combined) / max_combined
            writer.writerow({'AIRPORT': ap,
                            'PASSENGERS_FROM_CHINA': from_china,
                            'PASSENGERS_FROM_ITALY': from_italy,
                            'PASSENGERS_COMBINED': combined,
                            'BETA_CHINA': beta_china,
                            'BETA_ITALY': beta_italy,
                            'BETA_COMBINED': beta_combined,
                            'BETA_NORMALIZED': 1
                            })




def international_arrivals_main():
    print("Parsing international arrivals data...")
    airports = get_airports_from_csv()
    states_abbreviations = get_states_abbreviations_from_csv()

    states_count_china = get_count_by_category(FROM_CHINA_CSV, 'DEST_STATE')
    states_count_italy = get_count_by_category(FROM_ITALY_CSV, 'DEST_STATE')
    states_count_combined = get_combined_count(states_abbreviations.keys(), states_count_china, states_count_italy)

    airports_count_china = get_count_by_category(FROM_CHINA_CSV, 'DEST_CITY')
    airports_count_italy = get_count_by_category(FROM_ITALY_CSV, 'DEST_CITY')
    airports_count_combined = get_combined_count(airports, airports_count_china, airports_count_italy)

    max_china = max(airports_count_china.values())
    max_italy = max(airports_count_italy.values())
    max_combined = max(airports_count_combined.values())

    write_output_states(states_abbreviations, states_count_china, states_count_italy, states_count_combined)
    write_output_airports(airports, airports_count_china, airports_count_italy, airports_count_combined, max_china, max_italy, max_combined)
    print("International arrivals data parsing complete")
