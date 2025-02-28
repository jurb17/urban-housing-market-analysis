import pandas as pd
from data import months_list


# import original employment values into pandas dataframe
original_employment_df = pd.read_csv("employment_nonfarm_nychist.csv")
# remove unwanted columns
unwanted_columns = ["AREA", "SERIESCODE", "AREANAME", "INDUSTRY_TITLE"]
new_emp_df = original_employment_df.drop(columns=unwanted_columns)
# reverse order of dataframe rows:
new_emp_df = new_emp_df.iloc[::-1]
print(new_emp_df.head())

# create dataframe structure to store data
data = {
    "year": [],
    "month": [],
    "employment": [],
    "difference": [],
    "percent change": [],
}
employment_df = pd.DataFrame(data)

# add "Annual" to months_list
months_list.append("Annual")

# iterate through rows and then columns to organize data into prep state.
for index, row in new_emp_df.iterrows():
    temp_dict = {"year": row["YEAR"]}
    print(index, row["YEAR"])

    # track column index per row
    column_index = 0
    for item in row:
        print(item)
        if column_index > 0:
            # grab month string from list
            month = months_list[column_index - 1]
            # grab the employment value for that month
            value = item
            # find the difference between this year and last year, incl. percent change
            if index >= new_emp_df.shape[0] - 1:
                difference = "n/a"
                percent_change = "n/a"
            else:
                difference = round(
                    value
                    - float(
                        new_emp_df.iloc[
                            new_emp_df.shape[0] - (index + 2),
                            column_index,
                        ]
                    ),
                    2,
                )
                percent_change = round(
                    difference
                    / float(
                        new_emp_df.iloc[
                            new_emp_df.shape[0] - (index + 2),
                            column_index,
                        ]
                    )
                    * 100,
                    2,
                )

            # print the data for the new row
            print(row["YEAR"], month, value, difference, percent_change)
            new_row = {
                "year": row["YEAR"],
                "month": month,
                "employment": value,
                "difference": difference,
                "percent change": percent_change,
            }

            employment_df.loc[employment_df.shape[0]] = new_row

        # iterate over column index to get next month's data
        column_index += 1


print(employment_df.head(20))
employment_df.to_csv("employment-prep.csv", index=False)
