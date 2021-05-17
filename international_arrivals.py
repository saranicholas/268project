import csv
import numpy as np
from decimal import Decimal

AIRPORTS_CSV = 'data/in/airports.csv'

# FROM_ITALY_CSV = 'data/in/flights_from_italy.csv'
STATES_ABBREV_CSV = 'data/in/states_abbreviations.csv'
INTL_FLIGHTS_CSV = 'data/in/intl_flights.csv'

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


def get_count_by_category(arrivals_csv, category, countries):
    count = dict()
    with open(arrivals_csv, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ORIGIN_STATE'] in countries:
                if row[category] in count.keys():
                    count[row[category]] += int(row['PASSENGERS'])
                else:
                    count[row[category]] = int(row['PASSENGERS'])
    return count


def write_output_states(states_abbreviations, states_count_italy, states_count_europe):
    max_italy = max(states_count_italy.values())
    max_europe = max(states_count_europe.values())
    with open(STATES_CSV_OUT, 'w') as csvfile:
        fieldnames = ['STATE', 'STATE_ABBREVIATION', 'PASSENGERS_FROM_ITALY', 'PASSENGERS_FROM_ITALY_SCALED', 'PASSENGERS_FROM_ITALY_NEIGHBORS_SCALED']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for state in states_abbreviations.keys():
            from_italy = states_count_italy[state] if state in states_count_italy.keys() else 0
            from_italy_scaled = (1.0 * from_italy) / max_italy
            from_europe = states_count_europe[state] if state in states_count_europe.keys() else 0
            from_europe_scaled = (1.0 * from_europe) / max_europe
            writer.writerow({'STATE': states_abbreviations[state],
                            'STATE_ABBREVIATION': state,
                            'PASSENGERS_FROM_ITALY': from_italy,
                            'PASSENGERS_FROM_ITALY_SCALED': from_italy_scaled,
                            'PASSENGERS_FROM_ITALY_NEIGHBORS_SCALED': from_europe_scaled})


def write_output_airports(airports, airports_count_italy):
    max_italy = max(airports_count_italy.values())
    with open(AIRPORTS_CSV_OUT, 'w') as csvfile:
        fieldnames = ['AIRPORT', 'PASSENGERS_FROM_ITALY', 'BETA_ITALY', 'BETA_NORMALIZED']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ap in airports:
            from_italy = airports_count_italy[ap] if ap in airports_count_italy.keys() else 0
            beta_italy = (1.0 * from_italy) / max_italy
            writer.writerow({'AIRPORT': ap,
                            'PASSENGERS_FROM_ITALY': from_italy,
                            'BETA_ITALY': beta_italy,
                            'BETA_NORMALIZED': 1})




def international_arrivals_main():
    print("Parsing international arrivals data...")
    airports = get_airports_from_csv()
    states_abbreviations = get_states_abbreviations_from_csv()

    # states_count_italy = get_count_by_category(FROM_ITALY_CSV, 'DEST_STATE', {'Italy'})
    airports_count_italy = get_count_by_category(INTL_FLIGHTS_CSV, 'DEST_CITY', {'Italy'})
    states_count_italy = get_count_by_category(INTL_FLIGHTS_CSV, 'DEST_STATE', {'Italy'})
    states_count_europe = get_count_by_category(INTL_FLIGHTS_CSV, 'DEST_STATE', {'France', 'Switzerland', 'Austria', 'Slovenia'})

    write_output_states(states_abbreviations, states_count_italy, states_count_europe)
    write_output_airports(airports, airports_count_italy)
    print("International arrivals data parsing complete")
