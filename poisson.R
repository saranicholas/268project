covid_data <- read.csv("data/regression/regression_data.csv")

#BASELINE MODELS
poiss_baseline_17 = glm(CASES_MAR_17 ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_17_SCALED, family = "poisson", data = covid_data)
poiss_baseline_31 = glm(CASES_MAR_31 ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_31_SCALED, family = "poisson", data = covid_data)

poiss_baseline_europe_17 = glm(CASES_MAR_17 ~ PASSENGERS_FROM_EUROPE_SCALED + TESTS_MAR_17_SCALED, family = "poisson", data = covid_data)
poiss_baseline_europe_31 = glm(CASES_MAR_31 ~ PASSENGERS_FROM_EUROPE_SCALED + TESTS_MAR_31_SCALED, family = "poisson", data = covid_data)

#NEIGHBORS OF HUBS MODELS
poiss_neighbors_17 = glm(CASES_MAR_17 ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_17_SCALED + NEIGHBORS_HUBS_ITALY , family = "poisson", data = covid_data)
poiss_neighbors_31 = glm(CASES_MAR_31 ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_31_SCALED + NEIGHBORS_HUBS_ITALY , family = "poisson", data = covid_data)


#PAGE RANK MODELS
poiss_rank_normalized_17 = glm(CASES_MAR_17 ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_17_SCALED+ RANK_NORMALIZED, family = "poisson", data = covid_data)
poiss_rank_normalized_31 = glm(CASES_MAR_31 ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_31_SCALED + RANK_NORMALIZED, family = "poisson", data = covid_data)

poiss_rank_italy_17 = glm(CASES_MAR_17 ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_17_SCALED+ RANK_ITALY, family = "poisson", data = covid_data)
poiss_rank_italy_31 = glm(CASES_MAR_31 ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_31_SCALED + RANK_ITALY, family = "poisson", data = covid_data)


#MODEL SUMMARIES
summary(poiss_baseline_17)
summary(poiss_baseline_31)

summary(poiss_baseline_europe_17)
summary(poiss_baseline_europe_31)

summary(poiss_neighbors_17)
summary(poiss_neighbors_31)

summary(poiss_rank_normalized_17)
summary(poiss_rank_normalized_31)

summary(poiss_rank_italy_17)
summary(poiss_rank_italy_31)
