import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as web
import statsmodels.api as sm
start_date = "2010-01-01"#

interest_rate = web.DataReader("FEDFUNDS", "fred", start_date)
unemployment = web.DataReader("UNRATE", "fred", start_date)
gdp = web.DataReader("GDPC1", "fred", start_date)


interest_rate["QUARTER"] = interest_rate.index.to_period("Q")
unemployment["QUARTER"] = unemployment.index.to_period("Q")

interest_q = interest_rate.groupby("QUARTER")["FEDFUNDS"].mean()
unemp_q = unemployment.groupby("QUARTER")["UNRATE"].mean()

gdp_q = gdp["GDPC1"].copy()
gdp_q.index = gdp_q.index.to_period("Q")
gdp_growth = gdp_q.pct_change() * 100


df = pd.DataFrame({
    "FEDFUNDS": interest_q,
    "UNRATE": unemp_q,
    "GDP_GROWTH": gdp_growth
})

df["RATE_CHANGE"] = df["FEDFUNDS"].diff()
df["UNRATE_CHANGE"] = df["UNRATE"].diff()

df["RATE_CHANGE_LAG1"] = df["RATE_CHANGE"].shift(1)

data_clean = df.dropna().copy()

data_clean.index = data_clean.index.to_timestamp()


X = sm.add_constant(
    data_clean[["RATE_CHANGE", "GDP_GROWTH"]]
)

y = data_clean["UNRATE_CHANGE"]

model = sm.OLS(y, X).fit()

X_lag = sm.add_constant(
    data_clean[["RATE_CHANGE_LAG1", "GDP_GROWTH"]]
)

y_lag = data_clean["UNRATE_CHANGE"]

lag_model = sm.OLS(y_lag, X_lag).fit()


fig, axes = plt.subplots(1, 2, figsize=(14, 5))


axes[0].plot(
    data_clean.index,
    data_clean["FEDFUNDS"],
    label="Fed Funds Rate (%)"
)

axes[0].plot(
    data_clean.index,
    data_clean["UNRATE"],
    label="Unemployment Rate (%)"
)

axes[0].set_title("U.S. Interest Rates and Unemployment")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Percent")
axes[0].grid(True)
axes[0].legend()


axes[1].scatter(
    data_clean["GDP_GROWTH"],
    data_clean["UNRATE_CHANGE"],
    alpha=0.7
)

axes[1].set_title("GDP Growth vs. Change in Unemployment")
axes[1].set_xlabel("GDP Growth (%)")
axes[1].set_ylabel("Change in Unemployment Rate (%)")
axes[1].grid(True)

plt.tight_layout()
plt.show()


print("\n================ DATASET ================")
print(data_clean.head(10))

print("\nNumber of observations:")
print(len(data_clean))

print("\n================ CONTEMPORANEOUS MODEL ================")
print(model.summary())

print("\n================ LAGGED MODEL ================")
print(lag_model.summary())

pre_covid = data_clean[
    data_clean.index < "2020-01-01"
].copy()

covid_period = data_clean[
    data_clean.index >= "2020-01-01"
].copy()

X_pre = sm.add_constant(
    pre_covid[["RATE_CHANGE", "GDP_GROWTH"]]
)

y_pre = pre_covid["UNRATE_CHANGE"]

pre_model = sm.OLS(y_pre, X_pre).fit()

X_covid = sm.add_constant(
    covid_period[["RATE_CHANGE", "GDP_GROWTH"]]
)

y_covid = covid_period["UNRATE_CHANGE"]

covid_model = sm.OLS(y_covid, X_covid).fit()

print("\n================ PRE-COVID MODEL ================")
print(pre_model.summary())

print("\n================ COVID/POST-COVID MODEL ================")
print(covid_model.summary())


import numpy as np



plt.figure(figsize=(12, 6))

plt.plot(
    data_clean.index,
    data_clean["FEDFUNDS"],
    label="Federal Funds Rate"
)

plt.plot(
    data_clean.index,
    data_clean["UNRATE"],
    label="Unemployment Rate"
)

plt.title("U.S. Interest Rates and Unemployment, 2010–2026")
plt.xlabel("Year")
plt.ylabel("Percent")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()




plt.figure(figsize=(8, 6))

plt.scatter(
    data_clean["GDP_GROWTH"],
    data_clean["UNRATE_CHANGE"],
    alpha=0.7
)

# Regression line
x = data_clean["GDP_GROWTH"]

z = np.polyfit(
    x,
    data_clean["UNRATE_CHANGE"],
    1
)

line = np.poly1d(z)

plt.plot(
    x,
    line(x),
    label="Regression Line"
)

plt.title("GDP Growth vs. Change in Unemployment")
plt.xlabel("GDP Growth (%)")
plt.ylabel("Change in Unemployment Rate (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()




predicted = model.predict(
    sm.add_constant(
        data_clean[["RATE_CHANGE", "GDP_GROWTH"]]
    )
)

plt.figure(figsize=(12, 6))

plt.plot(
    data_clean.index,
    data_clean["UNRATE_CHANGE"],
    label="Actual"
)

plt.plot(
    data_clean.index,
    predicted,
    label="Predicted"
)

plt.axhline(
    y=0,
    linestyle="--"
)

plt.title("Actual vs. Predicted Changes in Unemployment")
plt.xlabel("Year")
plt.ylabel("Change in Unemployment Rate (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()