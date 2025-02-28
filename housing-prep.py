import pandas as pd
import calendar


# Convert 2-digit month to full name
def convert_month(month_num):
    return calendar.month_name[int(month_num)]


# import original employment values into pandas dataframe
original_housing_df = pd.read_csv(
    "nyc housing prices Metro_zhvi_uc_sfrcondo_tier_0.0_0.33_sm_sa_month.csv"
)
print(original_housing_df.head())

# create dataframe structure to store data
data = {
    "year": [],
    "month": [],
    "housing price": [],
    "annual housing price change": [],
}
housing_df = pd.DataFrame(data)

# iterate through rows
for index, row in original_housing_df.iterrows():
    # take "date" column value and separate year and month values
    month = row["date"].split("-")[1]
    year = row["date"].split("-")[0]
    # translate month value to full name of month
    month = convert_month(month)

    # determine difference and percent change between this year and last year
    if index < 12:
        price_difference = "n/a"
        price_percent_change = "n/a"
    else:
        housing_price_last_year = float(original_housing_df.iloc[index - 12]["ny"])
        price_difference = round(row["ny"] - housing_price_last_year, 2)
        price_percent_change = round(
            price_difference / housing_price_last_year * 100, 2
        )

    # add data to dataframe
    new_row = {
        "year": year,
        "month": month,
        "housing price": row["ny"],
        "annual housing price change": price_percent_change,
    }
    print(new_row)

    housing_df.loc[housing_df.shape[0]] = new_row

# print first 20 rows of dataframe and save to new svg file.
print(housing_df.head(20))
housing_df.to_csv("housing-prep.csv", index=False)
