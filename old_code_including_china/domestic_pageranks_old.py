import csv
import numpy as np
from decimal import Decimal

FLIGHTS_CSV = 'data/in/domestic_flights.csv'
AIRPORTS_CSV = 'data/in/airports.csv'
BETA_CSV = 'data/out/intl_arrivals_by_airport.csv'
RANKS_CSV_OUT = 'data/out/airport_pageranks.csv'


# FLIGHTS_CSV = 'data/example/network.csv'
# AIRPORTS_CSV = 'data/example/nodes.csv'
# BETA_CSV = 'data/example/beta.csv'
# RANKS_CSV_OUT = 'data/example/network_out.csv'

def get_airports_from_csv():
    airports = []
    with open(AIRPORTS_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            airports.append(row['AIRPORT'])
    return airports

def get_airports_dict(airports):
    airport_to_index = dict()
    for i in range(len(airports)):
        airport_to_index[airports[i]] = i
    return airport_to_index

def get_routes_from_csv():
    routes = dict()
    with open(FLIGHTS_CSV, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                routes[row['ROUTE']] = int(row['PASSENGERS'])
    return routes

def get_out_degrees_from_csv(airports, airport_to_index):
    out_degrees = [0] * len(airports)
    with open(FLIGHTS_CSV, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['ORIGIN_CITY'] in airport_to_index.keys():
                    airport_index = airport_to_index[row['ORIGIN_CITY']]
                    out_degrees[airport_index] += int(row['PASSENGERS'])
    return out_degrees

def get_in_degrees_from_csv(airports, airport_to_index):
    in_degrees = [0] * len(airports)
    with open(FLIGHTS_CSV, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['DEST_CITY'] in airport_to_index.keys():
                    airport_index = airport_to_index[row['DEST_CITY']]
                    in_degrees[airport_index] += int(row['PASSENGERS'])
    return in_degrees

def get_degree_normalization(out_degrees, in_degrees):
    n = len(out_degrees)
    degree_normalization = [0] * n
    for i in range(n):
        if out_degrees[i] == 0 and in_degrees[i] == 0:
            degree_normalization[i] = 1
        else:
            degree_normalization[i] = max(out_degrees[i], in_degrees[i])
    return degree_normalization


def construct_coeff_matrix(routes, airports, degree_normalization):
    n = len(airports)
    g = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            current_route = airports[j] + ' - ' + airports[i]
            if i == j:
                g[i,j] = 1.0
            elif current_route in routes:
                g[i,j] = -1.0 * routes[current_route] / degree_normalization[j]
    return g

def get_beta_from_csv(airport_to_index, beta_type):
    n = len(airport_to_index)
    beta = np.zeros(n)
    with open(BETA_CSV, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['AIRPORT'] in airport_to_index.keys():
                    beta[airport_to_index[row['AIRPORT']]] = Decimal(row[beta_type])
    return beta

def compute_ranks(coeff_matrix, beta):
    ranks = np.linalg.solve(coeff_matrix, beta)
    return ranks


def write_output(airports, ranks_normalized, ranks_china, ranks_italy, ranks_combined):
    with open(RANKS_CSV_OUT, 'w') as csvfile:
        fieldnames = ['AIRPORT', 'RANK_NORMALIZED', 'RANK_CHINA', 'RANK_ITALY', 'RANK_COMBINED']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(airports)):
            writer.writerow({'AIRPORT': airports[i],
                            'RANK_NORMALIZED': ranks_normalized[i],
                            'RANK_CHINA': ranks_china[i],
                            'RANK_ITALY': ranks_italy[i],
                            'RANK_COMBINED': ranks_combined[i]})


def compute_ranks_by_type(airport_to_index, coeff_matrix, beta_type):
    beta = get_beta_from_csv(airport_to_index, beta_type)
    ranks = compute_ranks(coeff_matrix, beta)
    return ranks





def domestic_pageranks_main():
    print("Computing airport page ranks...")
    airports = get_airports_from_csv()
    airport_to_index = get_airports_dict(airports)
    routes = get_routes_from_csv()

    out_degrees = get_out_degrees_from_csv(airports, airport_to_index)
    in_degrees = get_in_degrees_from_csv(airports, airport_to_index)
    degree_normalization = get_degree_normalization(out_degrees, in_degrees)
    coeff_matrix = construct_coeff_matrix(routes, airports, degree_normalization)

    ranks_normalized = compute_ranks_by_type(airport_to_index, coeff_matrix, 'BETA_NORMALIZED')
    ranks_china = compute_ranks_by_type(airport_to_index, coeff_matrix, 'BETA_CHINA')
    ranks_italy = compute_ranks_by_type(airport_to_index, coeff_matrix, 'BETA_ITALY')
    ranks_combined = compute_ranks_by_type(airport_to_index, coeff_matrix, 'BETA_COMBINED')

    write_output(airports, ranks_normalized, ranks_china, ranks_italy, ranks_combined)
    print("Airport page rank computation complete")
