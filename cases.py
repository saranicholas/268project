import csv

CASES_BY_DATE_BY_STATE_CSV = 'data/in/covid_cases.csv'
STATES_ABBREV_CSV = 'data/in/states_abbreviations.csv'

CASES_CSV_OUT = 'data/out/state_cases.csv'

def get_cases_from_csv(specified_date, state_to_abbreviations):
    states_to_case_counts = dict()
    with open(CASES_BY_DATE_BY_STATE_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['date'] == specified_date:
                states_to_case_counts[row['state']] = int(row['cases'])
    return states_to_case_counts


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



def cases_main():
    print("Cleaning COVID case count data...")
    states_to_abbreviations = get_states_abbreviations_from_csv_reversed()

    case_count_mar17 = get_cases_from_csv('2020-03-17', states_to_abbreviations)
    case_count_mar31 = get_cases_from_csv('2020-03-31', states_to_abbreviations)

    write_output_cases(states_to_abbreviations, case_count_mar17, case_count_mar31)
    print("COVID case count data cleaning complete")
