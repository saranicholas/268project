import csv
import numpy as np
from decimal import Decimal

FLIGHTS_CSV = 'data/flight_data.csv'
AIRPORTS_CSV = 'data/airports.csv'
BETA_CSV = 'data/intl_ranks.csv'
RANKS_CSV_OUT = 'data/domestic_ranks.csv'


# FLIGHTS_CSV = 'data/example/network.csv'
# AIRPORTS_CSV = 'data/example/nodes.csv'
# BETA_CSV = 'data/example/beta.csv'
# RANKS_CSV_OUT = 'data/example/network_out.csv'

def get_airports_from_csv():
    print("Extracting airport list...")
    airports = []
    with open(AIRPORTS_CSV, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            airports.append(row['AIRPORT'])
    print("Airport list extraction complete")
    return airports

def get_airports_dict(airports):
    print("Creating airport dictionary...")
    airport_to_index = dict()
    for i in range(len(airports)):
        airport_to_index[airports[i]] = i
    print("Airport dictionary creation complete")
    return airport_to_index

def get_routes_from_csv():
    print("Extracting routes...")
    routes = dict()
    with open(FLIGHTS_CSV, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # print(row)
                routes[row['ROUTE']] = int(row['PASSENGERS'])
    print("Route extraction complete")
    return routes

def get_out_degrees_from_csv(airports):
    print("Calculating out-degrees...")
    out_degrees = [0] * len(airports)
    with open(FLIGHTS_CSV, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['ORIGIN_CITY'] in airport_to_index.keys():
                    airport_index = airport_to_index[row['ORIGIN_CITY']]
                    out_degrees[airport_index] += int(row['PASSENGERS'])
    print("Out-degree calculation complete")
    return out_degrees

def get_in_degrees_from_csv(airports):
    print("Calculating in-degrees...")
    in_degrees = [0] * len(airports)
    with open(FLIGHTS_CSV, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['DEST_CITY'] in airport_to_index.keys():
                    airport_index = airport_to_index[row['DEST_CITY']]
                    in_degrees[airport_index] += int(row['PASSENGERS'])
    print("In-degree calculation complete")
    return in_degrees

def get_degree_normalization(out_degrees, in_degrees):
    print("Calculating degree normalizations...")
    n = len(out_degrees)
    degree_normalization = [0] * n
    for i in range(n):
        if out_degrees[i] == 0 and in_degrees[i] == 0:
            degree_normalization[i] = 1
        else:
            degree_normalization[i] = max(out_degrees[i], in_degrees[i])
    return degree_normalization
    print("Degree normalization calculation complete")


def construct_coeff_matrix(routes, airports, degree_normalization):
    print("Constructing coefficient matrix...")
    n = len(airports)
    g = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            current_route = airports[j] + ' - ' + airports[i]
            if i == j:
                g[i,j] = 1.0
            elif current_route in routes:
                g[i,j] = -1.0 * routes[current_route] / degree_normalization[j]
    print("Coefficient matrix construction complete")
    return g

def get_beta_from_csv(airport_to_index):
    print("Extracting beta vector...")
    n = len(airport_to_index)
    beta = np.zeros(n)
    with open(BETA_CSV, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['AIRPORT'] in airport_to_index.keys():
                    beta[airport_to_index[row['AIRPORT']]] = Decimal(row['BETA'])
    print("Beta vector extraction complete")
    return beta

def compute_ranks(coeff_matrix, beta):
    print("Computing ranks...")
    ranks = np.linalg.solve(coeff_matrix, beta)
    return ranks
    print("Rank computation complete")


def write_output(airports, ranks):
    print("Writing output...")
    with open(RANKS_CSV_OUT, 'w') as csvfile:
        fieldnames = ['AIRPORT', 'DOMESTIC_RANK']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(airports)):
            writer.writerow({'AIRPORT': airports[i], 'DOMESTIC_RANK': ranks[i]})
    print("Writing complete")

if __name__ == "__main__":
    airports = get_airports_from_csv()
    airport_to_index = get_airports_dict(airports)

    routes = get_routes_from_csv()

    out_degrees = get_out_degrees_from_csv(airports)
    in_degrees = get_in_degrees_from_csv(airports)
    degree_normalization = get_degree_normalization(out_degrees, in_degrees)

    coeff_matrix = construct_coeff_matrix(routes, airports, degree_normalization)
    print(coeff_matrix)
    beta = get_beta_from_csv(airport_to_index)

    ranks = compute_ranks(coeff_matrix, beta)

    write_output(airports, ranks)
