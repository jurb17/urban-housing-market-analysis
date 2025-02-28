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
    "difference (in thousands)": [],
    "percent change": [],
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
    # determine difference and percent change between this year and last year
    if index < 12:
        difference = "n/a"
        percent_change = "n/a"
    else:
        difference = round(
            row["Employment (000's)"]
            - float(original_employment_df.iloc[index - 12]["Employment (000's)"]),
            2,
        )
        percent_change = round(
            difference
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
        "difference (in thousands)": difference,
        "percent change": percent_change,
    }

    employment_df.loc[employment_df.shape[0]] = new_row

# print first 20 rows of dataframe and save to new svg file.
print(employment_df.head(20))
employment_df.to_csv("employment-SA-prep.csv", index=False)
