covid_data <- read.csv("data/regression/regression_data.csv")

#BASELINE MODELS
log_baseline_17 = lm(formula = log(CASES_MAR_17) ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_17_SCALED, data = covid_data)
log_baseline_31 = lm(formula = log(CASES_MAR_31) ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_31_SCALED, data = covid_data)

log_baseline_europe_17 = lm(formula = log(CASES_MAR_17) ~ PASSENGERS_FROM_EUROPE_SCALED + TESTS_MAR_17_SCALED, data = covid_data)
log_baseline_europe_31 = lm(formula = log(CASES_MAR_31) ~ PASSENGERS_FROM_EUROPE_SCALED + TESTS_MAR_31_SCALED, data = covid_data)

#NEIGHBORS OF HUBS MODELS
log_neighbors_17 = lm(formula = log(CASES_MAR_17) ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_17_SCALED + NEIGHBORS_HUBS_ITALY, data = covid_data)
log_neighbors_31 = lm(formula = log(CASES_MAR_31) ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_31_SCALED + NEIGHBORS_HUBS_ITALY, data = covid_data)

#PAGE RANK MODELS
log_rank_normalized_17 = lm(formula = log(CASES_MAR_17) ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_17_SCALED+ RANK_NORMALIZED, data = covid_data)
log_rank_normalized_31 = lm(formula = log(CASES_MAR_31) ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_31_SCALED + RANK_NORMALIZED, data = covid_data)

log_rank_italy_17 = lm(formula = log(CASES_MAR_17) ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_17_SCALED+ RANK_ITALY, data = covid_data)
log_rank_italy_31 = lm(formula = log(CASES_MAR_31) ~ PASSENGERS_FROM_ITALY_SCALED + TESTS_MAR_31_SCALED + RANK_ITALY, data = covid_data)


#MODEL SUMMARIES
summary(log_baseline_17)
summary(log_baseline_31)

summary(log_baseline_europe_17)
summary(log_baseline_europe_31)

summary(log_neighbors_17)
summary(log_neighbors_31)

summary(log_rank_normalized_17)
summary(log_rank_normalized_31)

summary(log_rank_italy_17)
summary(log_rank_italy_31)

