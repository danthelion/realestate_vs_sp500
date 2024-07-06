import numpy as np
import pandas as pd
import numpy_financial as npf
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Parameters
# Real Estate Investment
property_value_initial = 50_000_000  # HUF
down_payment = 10_000_000  # HUF
loan_amount = property_value_initial - down_payment  # HUF
interest_rate = 0.065  # Annual interest rate for the loan
loan_term_years = 20
monthly_rent_income_initial = 150_000  # HUF
maintenance_cost = 30_000  # HUF per month
property_value_growth_rate = 0.04  # Annual growth rate
rent_growth_rate = 0.04  # Annual growth rate for rent
occupancy_rate = 0.90  # 90% occupancy rate (percentage)

# S&P 500 Investment
initial_investment = 5_000_000  # HUF
sp500_growth_rate = 0.10  # Annual growth rate
investment_term_years = 20

# Monthly property management cost
management_cost_monthly = monthly_rent_income_initial * 0.10  # 10% of monthly rent income

# Monthly mortgage payment calculation
n_payments = loan_term_years * 12
monthly_interest_rate = interest_rate / 12
# monthly_payment = npf.pmt(monthly_interest_rate, n_payments, -loan_amount)
monthly_payment = 300_000  # HUF

# Arrays to store results
property_values = np.zeros(loan_term_years)
property_equities = np.zeros(loan_term_years)
sp500_investment_values = np.zeros(loan_term_years)
total_rent_income = np.zeros(loan_term_years)
total_value = np.zeros(loan_term_years)  # New array for total real estate value

# Initial values
current_property_value = property_value_initial
current_loan_balance = loan_amount
current_equity = down_payment
current_sp500_value = initial_investment
current_rent_income = monthly_rent_income_initial

years = np.arange(1, loan_term_years + 1)

for year in range(loan_term_years):
    # Property value growth
    current_property_value *= (1 + property_value_growth_rate)
    property_values[year] = current_property_value

    # Calculate remaining loan balance and equity
    for month in range(12):
        current_loan_balance -= (monthly_payment - current_loan_balance * monthly_interest_rate)
        current_equity = current_property_value - current_loan_balance

    property_equities[year] = current_equity

    # Calculate total rent income with annual growth and deduct management cost
    effective_monthly_rent_income = monthly_rent_income_initial * occupancy_rate
    total_rent_income[year] = effective_monthly_rent_income * 12 - management_cost_monthly * 12
    current_rent_income *= (1 + rent_growth_rate)

    # Calculate total value (rent income + property equity)
    total_value[year] = total_rent_income[year] + current_equity

    # S&P 500 investment growth without monthly contributions
    for month in range(12):
        current_sp500_value *= (1 + sp500_growth_rate / 12)

    sp500_investment_values[year] = current_sp500_value

# Compile results into a DataFrame
df = pd.DataFrame({
    'Year': years,
    'Property Value (HUF)': property_values,
    'Property Equity (HUF)': property_equities,
    'S&P 500 Value (HUF)': sp500_investment_values,
    'Annual Rent Income (HUF)': total_rent_income,
    'Total Real Estate Value (HUF)': total_value  # New column added
})

print(df)

# Plotting Property Equity, Total Real Estate Value, and S&P 500 Investment Value
plt.figure(figsize=(10, 6))

# Plotting the lines
plt.plot(df['Year'], df['Property Equity (HUF)'], label='Property Equity (HUF)')
plt.plot(df['Year'], df['S&P 500 Value (HUF)'], label='S&P 500 Value (HUF)')

# Function to format y-axis ticks in millions
def millions_formatter(x, pos):
    return f'{x / 1_000_000:.0f}M'


# Adding text annotations for the values with tilt
for i in range(len(df)):
    plt.text(df['Year'][i], df['Property Equity (HUF)'][i],
             f"{millions_formatter(df['Property Equity (HUF)'][i], None)}", fontsize=8,
             ha='left', rotation=5)
    plt.text(df['Year'][i], df['S&P 500 Value (HUF)'][i], f"{millions_formatter(df['S&P 500 Value (HUF)'][i], None)}",
             fontsize=8, ha='left',
             rotation=5)

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Value (HUF)')
plt.title('Property Equity, Total Real Estate Value, and S&P 500 Investment Value Over Time')
plt.legend()
plt.grid(True)

# Apply the millions formatter to y-axis
formatter = FuncFormatter(millions_formatter)
plt.gca().yaxis.set_major_formatter(formatter)

# Scaling the y-axis properly
max_value = max(df['Property Equity (HUF)'].max(), df['Total Real Estate Value (HUF)'].max(),
                df['S&P 500 Value (HUF)'].max())
plt.ylim(0, max_value * 1.1)  # adding 10% padding to the top

plt.savefig('property_values2.png')

# Show the plot
plt.tight_layout()
plt.show()
