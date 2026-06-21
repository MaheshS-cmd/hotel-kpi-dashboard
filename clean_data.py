"""
Hotel Revenue Historical Dataset — Cleaning & Feature Engineering
-------------------------------------------------------------------
Source: hotel_revenue_historical_full.xlsx
Sheets: '2018', '2019', '2020' (raw booking-level records)
        'meal_cost', 'market_segment' (lookup/reference tables)

Output: hotel_kpi_clean.csv  -> ready for SQL load + Power BI import
"""

import pandas as pd

SRC = "hotel_revenue_historical_full.xlsx"
OUT = "hotel_kpi_clean.csv"

# Combining the yearly sheets into one

xls = pd.ExcelFile(SRC)
df = pd.concat(
    [pd.read_excel(xls, sheet_name=yr) for yr in ["2018", "2019", "2020"]],
    ignore_index=True,
)
print(f"Combined raw shape: {df.shape}")

# Joining the meal_cost and market_segment table

meal_cost = pd.read_excel(xls, sheet_name="meal_cost")
market_segment = pd.read_excel(xls, sheet_name="market_segment")

df = df.merge(meal_cost, on="meal", how="left")
df = df.merge(market_segment, on="market_segment", how="left")
df.rename(columns={"Cost": "meal_cost_per_night", "Discount": "channel_discount"}, inplace=True)

# To understand the actual arrival date

df["arrival_date"] = pd.to_datetime(
    df["arrival_date_year"].astype(str) + "-" +
    df["arrival_date_month"] + "-" +
    df["arrival_date_day_of_month"].astype(str),
    format="%Y-%B-%d",
    errors="coerce",
)

# Clear Dup rows

before = len(df)
df = df.drop_duplicates()
print(f"Dropped {before - len(df)} exact duplicate rows")

# Getting rid of '0' rate bookings (Could be house rate but not explicitly mentioned in the dataset) leaving the comp rate rooms,

df = df[~(df["adr"] < 0)]
df = df[~((df["adr"] == 0) & (df["market_segment"] != "Complementary"))]

# One ADR value of over 5k spotted, dropping this as no other similar high rate observed,

df.loc[df["adr"] > 1000, "adr"] = df["adr"].median()

# Getting rid of zero guest bookings

total_guests = df["adults"].fillna(0) + df["children"].fillna(0) + df["babies"].fillna(0)
df = df[total_guests > 0]

# No data in week and weekend nights columns, getting rid of all zero night stayed reservations,

total_nights_check = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
df = df[total_nights_check > 0]

# is_canceled vs reservation_status mismatch, ovrriding is_canceled values with reservation status and its more trustworthy

df.loc[df["reservation_status"] == "Check-Out", "is_canceled"] = 0

# hildren has 4 nulls

df["children"] = df["children"].fillna(0)

# country has missing values — label as 'Unknown' rather

df["country"] = df["country"].fillna("Unknown")

print(f"Shape after cleaning: {df.shape}")


# Trying to get some KPIs to build menaingful relationships later

# Total nights stayed
df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]

# Room revenue per booking = ADR x nights stayed

df["room_revenue"] = df["adr"] * df["total_nights"]
df.loc[df["is_canceled"] == 1, "room_revenue"] = 0

# Net revenue after channel discount/commission

df["channel_discount"] = df["channel_discount"].fillna(0)
df["net_revenue"] = df["room_revenue"] * (1 - df["channel_discount"])

# Total guests per booking

df["total_guests"] = df["adults"] + df["children"] + df["babies"]

# Room type mismatch

df["room_type_mismatch"] = (df["reserved_room_type"] != df["assigned_room_type"]).astype(int)

# Booking outcome flags, useful for cancellation-risk analysis
df["is_no_show"] = (df["reservation_status"] == "No-Show").astype(int)
df["is_checked_out"] = (df["reservation_status"] == "Check-Out").astype(int)


# Export

df.to_csv(OUT, index=False)
print(f"Saved cleaned file: {OUT}  ({df.shape[0]} rows, {df.shape[1]} columns)")
