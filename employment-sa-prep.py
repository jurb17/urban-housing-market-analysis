import pandas as pd
from data import months_list
import calendar


# Convert 3-letter abbreviation to full month name
def convert_month(abbr):
    return calendar.month_name[list(calendar.month_abbr).index(abbr)]


# import original employment values into pandas dataframe
original_employment_df = pd.read_csv("employment_seasonally_adjusted_nyclfsa.csv")
print(original_employment_df.head())

# create dataframe structure to store data
data = {
    "year": [],
    "month": [],
    "working-age population": [],
    "employment (in thousands)": [],
    "annual working-age population change": [],
    "annual employment change": [],
}
employment_df = pd.DataFrame(data)

# iterate through rows
for index, row in original_employment_df.iterrows():
    # take "YEAR" column value and separate year and month values
    month = row["YEAR"].split("-")[0]
    year = row["YEAR"].split("-")[1]
    # translate month value to full name of month
    month = convert_month(month)

    # translate year to 4-digit format
    if int(year) > 50:
        year = "19" + year
    else:
        year = "20" + year

    # determine working age population by dividing employment by employment-population ratio
    working_age_population = row["Employment (000's)"] / (row["Emp/Pop (%)"] / 100)
    working_age_population_last_year = float(
        original_employment_df.iloc[index - 12]["Employment (000's)"]
    ) / (float(original_employment_df.iloc[index - 12]["Emp/Pop (%)"]) / 100)

    # determine difference and percent change between this year and last year
    if index < 12:
        pop_difference = "n/a"
        pop_percent_change = "n/a"
        emp_difference = "n/a"
        emp_percent_change = "n/a"
    else:
        pop_difference = round(
            working_age_population - working_age_population_last_year, 2
        )
        pop_percent_change = round(
            pop_difference / working_age_population_last_year * 100, 2
        )
        emp_difference = round(
            row["Employment (000's)"]
            - float(original_employment_df.iloc[index - 12]["Employment (000's)"]),
            2,
        )
        emp_percent_change = round(
            emp_difference
            / float(original_employment_df.iloc[index - 12]["Employment (000's)"])
            * 100,
            2,
        )

    # add data to dataframe
    new_row = {
        "year": year,
        "month": month,
        "working-age population": working_age_population,
        "employment (in thousands)": row["Employment (000's)"],
        "annual working-age population change": pop_difference,
        "annual employment change": emp_difference,
    }

    employment_df.loc[employment_df.shape[0]] = new_row

# print first 20 rows of dataframe and save to new svg file.
print(employment_df.head(20))
employment_df.to_csv("employment-SA-prep.csv", index=False)
