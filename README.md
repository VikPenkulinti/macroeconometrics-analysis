 Macroeconomic Analysis: Interest Rates, GDP, and Unemployment

Overview

This project examines the relationship between U.S. interest rates, economic growth, and unemployment from 2010 through 2026. Using economic data from the Federal Reserve Economic Data (FRED) database, the project applies statistical analysis and ordinary least squares (OLS) regression to investigate how changes in monetary policy and GDP growth are associated with changes in unemployment.

The analysis also compares the relationship between these variables before and after the COVID-19 pandemic and examines whether changes in interest rates have a lagged relationship with unemployment.

 Research Questions

* How are changes in the Federal Funds Rate associated with changes in unemployment?
* How is GDP growth associated with changes in unemployment?
* Do changes in interest rates have a delayed relationship with unemployment?
* Did these relationships differ before and after the COVID-19 pandemic?

 Data

The project uses three FRED economic series:

* **FEDFUNDS** — Effective Federal Funds Rate
* **UNRATE** — U.S. Unemployment Rate
* **GDPC1** — Real Gross Domestic Product

The analysis begins in January 2010. Monthly interest-rate and unemployment data are converted to quarterly averages, while quarterly GDP data is converted into percentage growth.

 Methodology

The project uses Python and several statistical techniques:

1. Collects economic data directly from FRED.
2. Converts monthly interest-rate and unemployment observations into quarterly averages.
3. Calculates quarterly GDP growth.
4. Calculates quarterly changes in the Federal Funds Rate and unemployment rate.
5. Uses OLS regression to estimate the relationship between:

   * Change in unemployment
   * Change in the Federal Funds Rate
   * GDP growth
6. Builds a lagged regression model to examine whether previous-quarter interest-rate changes are associated with current changes in unemployment.
7. Separates the dataset into pre-COVID and COVID/post-COVID periods for comparison.
8. Creates visualizations comparing interest rates, unemployment, GDP growth, and model predictions.

 Regression Models

Contemporary Model

The primary model estimates:

**Change in Unemployment = β₀ + β₁(Change in Federal Funds Rate) + β₂(GDP Growth) + ε**

 Lagged Model

A second model examines whether the previous quarter's interest-rate change is associated with the current change in unemployment:

**Change in Unemployment = β₀ + β₁(Lagged Rate Change) + β₂(GDP Growth) + ε**

Visualizations

The project produces several visualizations, including:

* U.S. Federal Funds Rate and unemployment over time
* GDP growth versus changes in unemployment
* A regression line showing the relationship between GDP growth and unemployment changes
* Actual versus predicted changes in unemployment

 Pre-COVID vs. COVID/Post-COVID Analysis

To investigate whether macroeconomic relationships changed during the pandemic period, the data is divided into:

* **Pre-COVID:** Before January 2020
* **COVID/Post-COVID:** January 2020 onward

Separate OLS regression models are estimated for each period and compared.

Technologies Used

* **Python**
* **Pandas** — Data manipulation and analysis
* **Matplotlib** — Data visualization
* **Pandas DataReader** — Accessing FRED data
* **Statsmodels** — OLS regression and statistical analysis
* **NumPy** — Numerical calculations

## Project Structure

```text
macroeconometrics-analysis/
│
├── macroeconometrics.py
├── README.md
└── .gitignore
```

## How to Run

Install the required Python packages:

```bash
pip install pandas matplotlib pandas-datareader statsmodels numpy
```

Then run:

```bash
python macroeconometrics.py
```

The program will retrieve the latest available FRED observations beginning in 2010, perform the analysis, display the visualizations, and print the regression results.

 Limitations

This project investigates statistical associations rather than proving that changes in interest rates or GDP directly cause changes in unemployment. Macroeconomic relationships can be influenced by many additional factors, including inflation, fiscal policy, financial conditions, and unexpected economic shocks.

The COVID-19 period also represents an unusually large structural disruption, so relationships estimated during this period may not be directly comparable with normal economic conditions.

Purpose

This project was developed as an independent exploration of econometrics and economic data analysis. It combines economic theory, programming, statistical modeling, and data visualization to investigate real-world macroeconomic relationships.

 Data Source

Federal Reserve Bank of St. Louis — Federal Reserve Economic Data (FRED).

---

*This project is intended for educational and research purposes.*

