# Real Estate Net Present Value Analyzer
## Understanding Net Present Value (NPV)

We are using the Net Present Value (NPV) model for evaluating whether the investment is worthwhile or not. NVP looks at the investment's future cash flows and discounts them. The NPV is great for evaluating an investment property as it takes into consideration time value of money, future cash flows, and opportunity cost of other investments (discount rate). The limitations of this model, like all models, is that it makes assumptions of the numbers, such as risk free rate and home appreciation. It does not also model other external risks associated with owning an investment property. This model just looks at the cash flows. 

In short, **if NVP is positive, the investment is worth taking. Otherwise, the investment is not worthwhile**

[Read about NPV here](https://www.investopedia.com/terms/n/npv.asp#:~:text=Net%20present%20value%20(NPV)%20is,a%20projected%20investment%20or%20project.)

## Using the script 
Make sure you have all the dependencies installed. I didn't make a requirements.txt, but the only one you might need to install is Pandas. 

Clone the NPV Demo Notebook (Jupyter notebook), where I did a sample analysis of an Arizona property. We use the `NPV()` object and initialize it with a bunch of parameters.

```
import npv as net_present_value
parameters = {
    'home_price': 445000, 
    'percent_down': 0.2, 
    'mortgage_interest': 0.069, 
    'mortgage_length': 30, 
    'other_monthly_cost': 430,
    'monthly_rental_income': 2300, 
    'annual_rental_income_appreciation': 0.02, 
    'annual_home_appreciation': .03, 
    'investment_duration': 10, 
    'discount_rate': .05,
    'selling_fee': .06
}
npv = net_present_value.NPV(**parameters)
mortgage = npv.MORTGAGE
```

Replace the values of the parameters with your property's values. This is just a model that uses hypothetical values, so give your best guess for some values such as annual home appreciation and rental income. 

| Parameter                   |  Meaning |
| :----------------      | ------: |
| Home price              |   Home price in $$ |  
| Percentage down payment |   Percent down as a decimal |
| Mortgage Interest Rate       |  Mortgage interest as decimal |
| Mortgage Length           |  Mortgage length in years  |
| Additional Monthly Cost (HOA, Taxes, Insurance) | in dollars |
| Monthly Rental Income   |  Estimated monthly rental income |
| Anual Home Appreciation        |  Estimated home appreciation as a decimal |
| Anual Rental Income Appreciation |  Estimated rental income appreciation as a decimal|
| Investment Duration              |  How long you plan to hold this property |
| Discount rate (min required return)    | Benchmark returns |
| Sales Fee          |  Realtor fees and other fees at time of sale, as a decimal |


## The NPV object
After running this, you've created your NPV object 
```
npv = net_present_value.NPV(**parameters)
```

You can look at the mortgage structure by running 
```
npv.summarize_mortgage()
```

Running this will summarize your cash flows
```
npv.annual_cash_flows_df()
```

Get a summary of the NPV analysis
```
npv.summarize_df()
```

Take a look at the demo notebook to see what you can do with the `NPV` and `Mortgage` objects. 