import math
import decimal
import mortgage
from itertools import islice
import pandas as pd

MONTHS_IN_YEAR = 12

def prRed(skk): print("\033[91m{}\033[00m".format(skk))
def prGreen(skk): print("\033[92m{}\033[00m".format(skk))

class NPV: 
    def __init__(self, home_price, percent_down, mortgage_interest, mortgage_length, other_monthly_cost, monthly_rental_income, annual_rental_income_appreciation, annual_home_appreciation, investment_duration, discount_rate, selling_fee):
        self.HOME_PRICE = float(home_price)
        self.PERCENT_DOWN = float(percent_down)
        self.MORTGAGE_INTEREST = float(mortgage_interest)
        self.MORTGAGE_LENGTH = int(mortgage_length)
        self.OTHER_MONTHLY_COST = float(other_monthly_cost)
        self.MONTHLY_RENTAL_INCOME = float(monthly_rental_income)
        self.ANNUAL_RENTAL_INCOME_APPRECIATION = float(annual_rental_income_appreciation)
        self.ANNUAL_HOME_APPRECIATION = float(annual_home_appreciation)
        self.DISCOUNT_RATE = float(discount_rate)
        self.INVESTMENT_DURATION = int(investment_duration)
        self.SELLING_FEE = float(selling_fee)

        self.MORTGAGE = mortgage.Mortgage(interest=self.MORTGAGE_INTEREST, amount=self.loan_amount(), months=self.MORTGAGE_LENGTH * MONTHS_IN_YEAR)
    
    def down_payment(self): 
        return self.HOME_PRICE * self.PERCENT_DOWN
    
    def loan_amount(self): 
        return self.HOME_PRICE * (1 - self.PERCENT_DOWN)
    
    def monthly_payment(self): 
        mortgage_payment = float(self.MORTGAGE.monthly_payment())
        return mortgage_payment + self.OTHER_MONTHLY_COST
    
    def annual_discount_cash_flow(self, period): 
        return 12 * (self.MONTHLY_RENTAL_INCOME * math.pow((1 + self.ANNUAL_RENTAL_INCOME_APPRECIATION), int(period)) - self.monthly_payment()) / math.pow((1 + self.DISCOUNT_RATE), int(period))
    
    def annual_cash_flow(self, period): 
        return 12 * (self.MONTHLY_RENTAL_INCOME * math.pow((1 + self.ANNUAL_RENTAL_INCOME_APPRECIATION), int(period)) - self.monthly_payment())

    def final_discounted_cash_flow(self): 
        principle_paid = sum(float(month[0]) for month in islice(self.MORTGAGE.monthly_payment_schedule(), MONTHS_IN_YEAR * self.INVESTMENT_DURATION))
        principle_remaining = self.loan_amount() - principle_paid
        return ( self.final_home_price() * (1 - self.SELLING_FEE) - principle_remaining) / math.pow((1 + self.DISCOUNT_RATE), self.INVESTMENT_DURATION)
    
    def final_cash_flow(self): 
        principle_paid = sum(float(month[0]) for month in islice(self.MORTGAGE.monthly_payment_schedule(), MONTHS_IN_YEAR * self.INVESTMENT_DURATION))
        principle_remaining = self.loan_amount() - principle_paid
        return ( self.final_home_price() * (1 - self.SELLING_FEE) - principle_remaining)

    def final_home_price(self): 
        return self.HOME_PRICE * math.pow((1 + self.ANNUAL_HOME_APPRECIATION), self.INVESTMENT_DURATION)

    def annual_cash_flows_df(self): 
        year = []
        cash_flow = []
        discounted_cash_flow = []
        for yr in range(0, self.INVESTMENT_DURATION + 1): 
            year.append(yr)
            if yr == 0: 
                cash_flow.append(round(-self.down_payment(), 2))
                discounted_cash_flow.append(round(-self.down_payment(), 2))
            elif yr == self.INVESTMENT_DURATION: 
                cash_flow.append(round(self.final_cash_flow(), 2))
                discounted_cash_flow.append(round(self.final_discounted_cash_flow(), 2))
            else: 
                cash_flow.append(round(self.annual_cash_flow(period=yr), 2))
                discounted_cash_flow.append(round(self.annual_discount_cash_flow(period=yr), 2))
        data = {'year': year, 'cash_flow': cash_flow, 'discounted_cash_flow': discounted_cash_flow}

        df = pd.DataFrame(data=data)
        df = df.style.set_caption('Annual cash flows')
        
        return df
                

    def IRR(self): 
        npv = self.NPV()
        original_discount_rate = self.DISCOUNT_RATE
        if npv == 0: 
            return self.DISCOUNT_RATE
        if npv > 0: 
            while self.NPV() > 0: 
                self.DISCOUNT_RATE += 0.001
            irr = self.DISCOUNT_RATE
            self.DISCOUNT_RATE = original_discount_rate
            return round(irr, 3)
        else: 
            while self.NPV() < 0: 
                self.DISCOUNT_RATE -= 0.001
            irr = self.DISCOUNT_RATE
            self.DISCOUNT_RATE = original_discount_rate
            return round(irr, 3)

    def NPV(self): 
        NPV = 0
        NPV -= self.down_payment()

        for year in range(1, self.INVESTMENT_DURATION): 
            NPV += self.annual_discount_cash_flow(period=year)
        
        NPV += self.final_discounted_cash_flow()
        return round(NPV, 2)

    def summarize_df(self): 
        col_1 = ['Discount Rate (Benchmark)', 'Internal Rate of Return (IRR)',  'Net Present Value (NPV)'] 
        col_2 = [str(self.DISCOUNT_RATE * 100) + '%', str(self.IRR() * 100) + '%', '$' + str(self.NPV())]
        data = {'index': col_1, 'value': col_2}
        df = pd.DataFrame(data=data)
        df = df.style.set_caption('Investment Summary')

        if(self.NPV() > 0): 
            prGreen('This property beats the benchmark and is worth investing in')
        else: 
            prRed('This property underperforms the benchmark and is not worth investing')
        return df

    def summarize_mortgage(self):
        m = self.MORTGAGE
        print('{0:>25s}:  {1:>12.6f}'.format('Rate', m.rate()))
        print('{0:>25s}:  {1:>12.6f}'.format('Month Growth', m.month_growth()))
        print('{0:>25s}:  {1:>12.6f}'.format('APY', m.apy()))
        print('{0:>25s}:  {1:>12.0f}'.format('Payoff Years', m.loan_years()))
        print('{0:>25s}:  {1:>12.0f}'.format('Payoff Months', m.loan_months()))
        print('{0:>25s}:  {1:>12.2f}'.format('Amount', m.amount()))
        print('{0:>25s}:  {1:>12.2f}'.format('Monthly Payment', m.monthly_payment()))
        print('{0:>25s}:  {1:>12.2f}'.format('Annual Payment', m.annual_payment()))
        print('{0:>25s}:  {1:>12.2f}'.format('Total Payout', m.total_payout()))