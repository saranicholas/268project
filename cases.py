import csv
from international_arrivals import get_states_abbreviations_from_csv

CASES_BY_DATE_BY_STATE_CSV = 'data/in/covid_cases.csv'
STATES_ABBREV_CSV = 'data/in/states_abbreviations.csv'
TESTING_BY_DATE_BY_STATE_CSV = 'data/in/testing_data.csv'

CASES_CSV_OUT = 'data/out/state_cases.csv'
TESTING_CSV_OUT = 'data/out/state_testing.csv'

def get_counts_from_csv(cvs_file_counts, specified_date, state_to_abbreviations, category):
    states_to_counts = dict()
    with open(cvs_file_counts, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['date'] == specified_date:
                states_to_counts[row['state']] = int(row[category]) if row[category] != '' else 0
    return states_to_counts


def get_states_abbreviations_from_csv_reversed():
    states_to_abbreviations = dict()
    with open(STATES_ABBREV_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            states_to_abbreviations[row['STATE']] = row['STATE_ABBREVIATION']
    return states_to_abbreviations

def write_output_cases(states_to_abbreviations, case_count_mar17, case_count_mar31):
    with open(CASES_CSV_OUT, 'w') as csvfile:
        fieldnames = ['STATE', 'STATE_ABBREVIATION', 'CASES_MAR_17', 'CASES_MAR_31']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for state in states_to_abbreviations.keys():
            cases_mar17 = case_count_mar17[state] if state in case_count_mar17.keys() else 0
            cases_mar31 = case_count_mar31[state] if state in case_count_mar31.keys() else 0
            writer.writerow({'STATE': state,
                            'STATE_ABBREVIATION': states_to_abbreviations[state],
                            'CASES_MAR_17': cases_mar17,
                            'CASES_MAR_31': cases_mar31})

def write_output_testing(abbreviations_to_states, testing_mar17, testing_mar31):
    with open(TESTING_CSV_OUT, 'w') as csvfile:
        fieldnames = ['STATE', 'STATE_ABBREVIATION', 'TESTS_MAR_17_SCALED', 'TESTS_MAR_31_SCALED']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for state in abbreviations_to_states.keys():
            tests_mar17 = testing_mar17[state] if state in testing_mar17.keys() else 0
            tests_mar31 = testing_mar31[state] if state in testing_mar31.keys() else 0
            test_mar17_scaled = (1.0 * tests_mar17) / max(testing_mar17.values())
            test_mar31_scaled = (1.0 * tests_mar31) / max(testing_mar31.values())
            writer.writerow({'STATE': abbreviations_to_states[state],
                            'STATE_ABBREVIATION': state,
                            'TESTS_MAR_17_SCALED': test_mar17_scaled,
                            'TESTS_MAR_31_SCALED': test_mar31_scaled})



def cases_main():
    print("Cleaning COVID case count/testing data...")

    states_to_abbreviations = get_states_abbreviations_from_csv_reversed()
    abbreviations_to_states = get_states_abbreviations_from_csv()

    case_count_mar17 = get_counts_from_csv(CASES_BY_DATE_BY_STATE_CSV, '2020-03-17', states_to_abbreviations, 'cases')
    case_count_mar31 = get_counts_from_csv(CASES_BY_DATE_BY_STATE_CSV, '2020-03-31', states_to_abbreviations, 'cases')

    testing_mar17 = get_counts_from_csv(TESTING_BY_DATE_BY_STATE_CSV, '2020-03-17', states_to_abbreviations, 'totaltestresults')
    testing_mar31 = get_counts_from_csv(TESTING_BY_DATE_BY_STATE_CSV, '2020-03-31', states_to_abbreviations, 'totaltestresults')

    write_output_cases(states_to_abbreviations, case_count_mar17, case_count_mar31)
    write_output_testing(abbreviations_to_states, testing_mar17, testing_mar31)

    print("COVID case count/testing data cleaning complete")
