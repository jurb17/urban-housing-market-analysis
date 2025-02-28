import pandas as pd
import plotly.express as px

# import into pandas dataframe
employment_df = pd.read_csv("employment-SA-prep.csv")
print(employment_df.head())
housing_df = pd.read_csv("housing-prep.csv")
print(housing_df.head())

# convert month column to string
employment_df["month"] = employment_df["month"].astype(str)
housing_df["month"] = housing_df["month"].astype(str)
# convert year column to string
employment_df["year"] = employment_df["year"].astype(str)
housing_df["year"] = housing_df["year"].astype(str)

# combine the year and month columns into a single column
employment_df["date"] = employment_df["year"] + " " + employment_df["month"]
housing_df["date"] = housing_df["year"] + " " + housing_df["month"]

# combine the two dataframes on the date column
# merge the two dataframes on the date column
merge_df = employment_df.merge(housing_df, on="date", how="inner")
print(merge_df.head(25))
# exit()

# create a line chart that plots both the change in working-age population and employment
# over time
fig = px.line(
    merge_df,
    x="date",
    y=[
        "annual working-age population change",
        "annual employment change",
        "annual housing price change",
    ],
)
fig.show()
# save the plot as a png file
# fig.write_image("employment-housing-change.png")
