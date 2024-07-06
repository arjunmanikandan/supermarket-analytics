import pandas as pd
import os
from main import read_json,extract_csv_contents,main
from dotenv import load_dotenv

def display_write_df(products_profits_df):
    products_profits_df.to_csv("products_profits.csv",index=False)
    return products_profits_df

def get_max_profit(group):
    return group.loc[group["Profit($)"].idxmax()]

#Selling prices of all products calculated for 1000 units 
def calc_profit(csv_data,menu_total_cost_df,config):
    selling_prices_df = pd.merge(menu_total_cost_df,csv_data["selling_prices_data"],on=["Product"],how="left")
    selling_prices_df["SellingPrice($)Per1000Units"] =  selling_prices_df["SellingPrice($)"] * config["products_quantity"]
    selling_prices_df = selling_prices_df.rename(columns={"State_x":"BuyingFrom(State)","State_y":"SellingIn(State)"})
    selling_prices_df["Profit($)"] = selling_prices_df["SellingPrice($)Per1000Units"]-selling_prices_df["CostPrice($)"]
    selling_prices_df = selling_prices_df.groupby("Product").apply(get_max_profit,include_groups=False)
    return selling_prices_df.reset_index()

def product_profits():
    load_dotenv()
    config = read_json(os.getenv("CONFIG_PATH"))
    csv_data = extract_csv_contents(config)
    menu_total_cost_df = main()
    products_profits_df = calc_profit(csv_data,menu_total_cost_df,config)
    return display_write_df(products_profits_df)

if __name__ == "__main__":
    products_profits_df = product_profits()
    print(products_profits_df)
