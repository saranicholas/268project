from international_arrivals import international_arrivals_main
from domestic_pageranks import domestic_pageranks_main
from state_pageranks import state_pageranks_main


if __name__ == "__main__":
    print("Beginning data cleaning and generation...")
    international_arrivals_main()
    domestic_pageranks_main()
    state_pageranks_main()
    print("Data cleaning and generation complete")
