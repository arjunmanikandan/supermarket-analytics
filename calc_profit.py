import pandas as pd

def display_write_df(products_profits_df):
    products_profits_df.to_csv("products_profits.csv",index=False)
    return products_profits_df

def get_max_profit(group):
    max_profit_indexes = group.groupby(["Week"])["Profit($)"].idxmax().values
    return group.loc[max_profit_indexes]

#Selling prices of all products calculated for 1000 units 
def calc_profit(csv_data,menu_cost_price_df,config):
    selling_prices_df = pd.merge(menu_cost_price_df,csv_data["selling_prices_data"],on=["Product","Week"],how="left")
    selling_prices_df["SellingPrice($)Per1000Units"] =  selling_prices_df["SellingPrice($)"] * config["products_quantity"]
    selling_prices_df["Profit($)"] = selling_prices_df["SellingPrice($)Per1000Units"]-selling_prices_df["CostPrice($)"]
    selling_prices_df = selling_prices_df.rename(columns={"Location_x":"BuyingFrom(City)","Location_y":"SellingInState"})
    selling_prices_df = selling_prices_df.groupby("Product").apply(get_max_profit,include_groups=False)
    selling_prices_df = selling_prices_df.reset_index().drop(columns=["level_1"])
    return selling_prices_df

def product_profits(csv_data,menu_cost_price_df,config):
    products_profits_df = calc_profit(csv_data,menu_cost_price_df,config)
    return display_write_df(products_profits_df)