from Analysis import df_percentage_result
from Analysis import df_merge
from Analysis import df_city
from Analysis import df_country

df_percentage_result.to_csv(
    r"C:\Users\Kamil\Desktop\World_population_project\clean_data\df_percentage_result.csv", index=False)

df_merge.to_csv(
    r"C:\Users\Kamil\Desktop\World_population_project\clean_data\df_merge.csv", index=False)

df_city.to_csv(
    r"C:\Users\Kamil\Desktop\World_population_project\clean_data\df_city.csv", index=False)

df_country.to_csv(
    r"C:\Users\Kamil\Desktop\World_population_project\clean_data\df_country.csv", index=False)
