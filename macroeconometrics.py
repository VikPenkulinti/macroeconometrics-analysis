import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas_datareader import data as web
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from statsmodels.tsa.stattools import adfuller

# Create directory to save output plots
os.makedirs("plots", exist_ok=True)

start_date = "2010-01-01"

# Fetch FRED data
interest_rate = web.DataReader("FEDFUNDS", "fred", start_date)
unemployment = web.DataReader("UNRATE", "fred", start_date)
gdp = web.DataReader("GDPC1", "fred", start_date)

# Quarterly aggregation
interest_rate["QUARTER"] = interest_rate.index.to_period("Q")
unemployment["QUARTER"] = unemployment.index.to_period("Q")

interest_q = interest_rate.groupby("QUARTER")["FEDFUNDS"].mean()
unemp_q = unemployment.groupby("QUARTER")["UNRATE"].mean()

gdp_q = gdp["GDPC1"].copy()
gdp_q.index = gdp_q.index.to_period("Q")
gdp_growth = gdp_q.pct_change() * 100

# Build dataframe
df = pd.DataFrame(
    {"FEDFUNDS": interest_q, "UNRATE": unemp_q, "GDP_GROWTH": gdp_growth}
)
df["RATE_CHANGE"] = df["FEDFUNDS"].diff()
df["UNRATE_CHANGE"] = df["UNRATE"].diff()
df["RATE_CHANGE_LAG1"] = df["RATE_CHANGE"].shift(1)

data_clean = df.dropna().copy()
data_clean.index = data_clean.index.to_timestamp()

# ---------------------------------------------------------
# 1. Diagnostic Checks (Stationarity)
# ---------------------------------------------------------
print("================ STATIONARITY CHECKS (ADF TEST) ================")
for col in ["RATE_CHANGE", "GDP_GROWTH", "UNRATE_CHANGE"]:
  adf_res = adfuller(data_clean[col])
  print(f"{col} ADF Statistic: {adf_res[0]:.4f}, p-value: {adf_res[1]:.4f}")

# ---------------------------------------------------------
# 2. Fit OLS Models
# ---------------------------------------------------------
X = sm.add_constant(data_clean[["RATE_CHANGE", "GDP_GROWTH"]])
y = data_clean["UNRATE_CHANGE"]
model = sm.OLS(y, X).fit()

print("\n================ CONTEMPORANEOUS MODEL ================")
print(model.summary())
print(f"Durbin-Watson Statistic: {durbin_watson(model.resid):.4f}")

X_lag = sm.add_constant(data_clean[["RATE_CHANGE_LAG1", "GDP_GROWTH"]])
lag_model = sm.OLS(y, X_lag).fit()

print("\n================ LAGGED MODEL ================")
print(lag_model.summary())
print(f"Durbin-Watson Statistic: {durbin_watson(lag_model.resid):.4f}")

# Sub-sample splits
pre_covid = data_clean[data_clean.index < "2020-01-01"].copy()
covid_period = data_clean[data_clean.index >= "2020-01-01"].copy()

pre_model = sm.OLS(
    pre_covid["UNRATE_CHANGE"],
    sm.add_constant(pre_covid[["RATE_CHANGE", "GDP_GROWTH"]]),
).fit()
covid_model = sm.OLS(
    covid_period["UNRATE_CHANGE"],
    sm.add_constant(covid_period[["RATE_CHANGE", "GDP_GROWTH"]]),
).fit()

print("\n================ PRE-COVID MODEL SUMMARY ================")
print(pre_model.summary())
print("\n================ COVID/POST-COVID MODEL SUMMARY ================")
print(covid_model.summary())

# ---------------------------------------------------------
# 3. Export Visualizations to /plots
# ---------------------------------------------------------
# Plot 1: Rates vs Unemployment Time Series
plt.figure(figsize=(10, 5))
plt.plot(
    data_clean.index, data_clean["FEDFUNDS"], label="Federal Funds Rate (%)"
)
plt.plot(
    data_clean.index, data_clean["UNRATE"], label="Unemployment Rate (%)"
)
plt.title("U.S. Interest Rates and Unemployment (2010–Present)")
plt.xlabel("Year")
plt.ylabel("Percent")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/fed_funds_vs_unemployment.png", dpi=300)
plt.close()

# Plot 2: GDP Growth vs Unemployment Change Scatter & Fit
plt.figure(figsize=(8, 5))
plt.scatter(data_clean["GDP_GROWTH"], data_clean["UNRATE_CHANGE"], alpha=0.7)
x_val = data_clean["GDP_GROWTH"]
poly_fit = np.polyfit(x_val, data_clean["UNRATE_CHANGE"], 1)
plt.plot(x_val, np.poly1d(poly_fit)(x_val), color="red", label="OLS Fit")
plt.title("GDP Growth vs. Change in Unemployment")
plt.xlabel("GDP Growth (%)")
plt.ylabel("Change in Unemployment Rate (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/gdp_vs_unemployment_regression.png", dpi=300)
plt.close()

# Plot 3: Actual vs Predicted Unemployment Changes
predicted = model.predict(X)
plt.figure(figsize=(10, 5))
plt.plot(data_clean.index, data_clean["UNRATE_CHANGE"], label="Actual Change")
plt.plot(
    data_clean.index,
    predicted,
    label="Predicted Change",
    linestyle="--",
    color="orange",
)
plt.axhline(y=0, color="gray", linestyle=":")
plt.title("Actual vs. Predicted Changes in Unemployment")
plt.xlabel("Year")
plt.ylabel("Change in Unemployment Rate (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/actual_vs_predicted.png", dpi=300)
plt.close()

print("\n Execution complete. Figures saved to the /plots directory.")