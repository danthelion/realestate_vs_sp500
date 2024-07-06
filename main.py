import numpy as np
import pandas as pd
import numpy_financial as npf
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Parameters
# Real Estate Investment
property_value_initial_usd = 200_000  # Initial property value in USD
down_payment_usd = 50_000  # Down payment in USD
loan_amount_usd = property_value_initial_usd - down_payment_usd  # Loan amount in USD
interest_rate = 0.065  # Annual interest rate for the loan
loan_term_years = 20
monthly_rent_income_initial_usd = 500  # Initial monthly rent income in USD
maintenance_cost_usd = 100  # USD per month
property_value_growth_rate = 0.04  # Annual growth rate
rent_growth_rate = 0.04  # Annual growth rate for rent
occupancy_rate = 0.90  # 90% occupancy rate (percentage)

# S&P 500 Investment
initial_investment_usd = 50_000  # Initial investment in USD
sp500_growth_rate = 0.10  # Annual growth rate
investment_term_years = 20

# Monthly property management cost
management_cost_monthly_usd = monthly_rent_income_initial_usd * 0.10  # 10% of monthly rent income in USD

# Monthly mortgage payment calculation (using a fixed value for illustration)
n_payments = loan_term_years * 12
monthly_interest_rate = interest_rate / 12
monthly_payment_usd = 1500  # USD (placeholder value)

# Arrays to store results
property_values_usd = np.zeros(loan_term_years)
property_equities_usd = np.zeros(loan_term_years)
sp500_investment_values_usd = np.zeros(loan_term_years)
total_rent_income_usd = np.zeros(loan_term_years)
total_value_usd = np.zeros(loan_term_years)  # New array for total real estate value

# Initial values
current_property_value_usd = property_value_initial_usd
current_loan_balance_usd = loan_amount_usd
current_equity_usd = down_payment_usd
current_sp500_value_usd = initial_investment_usd
current_rent_income_usd = monthly_rent_income_initial_usd

years = np.arange(1, loan_term_years + 1)

for year in range(loan_term_years):
    # Property value growth
    current_property_value_usd *= (1 + property_value_growth_rate)
    property_values_usd[year] = current_property_value_usd

    # Calculate remaining loan balance and equity
    for month in range(12):
        current_loan_balance_usd -= (monthly_payment_usd - current_loan_balance_usd * monthly_interest_rate)
        current_equity_usd = current_property_value_usd - current_loan_balance_usd

    property_equities_usd[year] = current_equity_usd

    # Calculate effective monthly rent income and total rent income with annual growth
    effective_monthly_rent_income_usd = monthly_rent_income_initial_usd * occupancy_rate
    total_rent_income_usd[year] = effective_monthly_rent_income_usd * 12 - management_cost_monthly_usd * 12
    monthly_rent_income_initial_usd *= (1 + rent_growth_rate)

    # Calculate total value (rent income + property equity)
    total_value_usd[year] = total_rent_income_usd[year] + current_equity_usd

    # S&P 500 investment growth without monthly contributions
    for month in range(12):
        current_sp500_value_usd *= (1 + sp500_growth_rate / 12)

    sp500_investment_values_usd[year] = current_sp500_value_usd

# Compile results into a DataFrame
df = pd.DataFrame({
    'Year': years,
    'Property Value (USD)': property_values_usd,
    'Property Equity (USD)': property_equities_usd,
    'S&P 500 Value (USD)': sp500_investment_values_usd,
    'Annual Rent Income (USD)': total_rent_income_usd,
    'Total Real Estate Value (USD)': total_value_usd  # New column added
})

print(df)

# Plotting Property Equity, Total Real Estate Value, and S&P 500 Investment Value
plt.figure(figsize=(10, 6))

# Plotting the lines
plt.plot(df['Year'], df['Property Equity (USD)'], label='Property Equity (USD)')
plt.plot(df['Year'], df['S&P 500 Value (USD)'], label='S&P 500 Value (USD)')


# Function to format y-axis ticks in millions
def k_formatter(x, pos):
    return f'${x / 1_000:.0f}K'


# Adding text annotations for the values with tilt and millions formatter
for i in range(len(df)):
    plt.text(df['Year'][i], df['Property Equity (USD)'][i],
             f"{k_formatter(df['Property Equity (USD)'][i], None)}", fontsize=8,
             ha='left', rotation=5)
    plt.text(df['Year'][i], df['S&P 500 Value (USD)'][i], f"{k_formatter(df['S&P 500 Value (USD)'][i], None)}",
             fontsize=8, ha='left',
             rotation=5)

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Value (USD)')
plt.title('Property Equity, Total Real Estate Value, and S&P 500 Investment Value Over Time')
plt.legend()
plt.grid(True)

# Apply the millions formatter to y-axis
formatter = FuncFormatter(k_formatter)
plt.gca().yaxis.set_major_formatter(formatter)

# Scaling the y-axis properly
max_value_usd = max(df['Property Equity (USD)'].max(), df['Total Real Estate Value (USD)'].max(),
                    df['S&P 500 Value (USD)'].max())
plt.ylim(0, max_value_usd * 1.1)  # adding 10% padding to the top

plt.savefig('property_values3.png')

# Show the plot
plt.tight_layout()
plt.show()
