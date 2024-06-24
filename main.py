#Calculated Price Inclusive of taxes for each product
import pandas as pd
import sys,json

def read_json(json_path):
    with open(json_path,"r") as file:
        file_paths = json.load(file)
    return file_paths

def read_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df

def display_fare_details(fare_details_df):
    print(fare_details_df)

def calc_cost_details(row,super_market_df,menu):
    min_rate = super_market_df[super_market_df["Product"] == row["Product"]]["min"].values[0]
    menu.at[row.name,"MinimumRate"] =  min_rate
    return row["Quantity"] * min_rate

def calc_tax_details(price,tax):
    return price*tax+price

def get_cost_details(supermarket_products, menu):
    supermarket_products["min"] = supermarket_products[["SevenEleven($)","Walmart($)","Tesco($)"]].min(axis=1)
    menu["Price"] = menu.apply(calc_cost_details,args=(supermarket_products,menu),axis=1)
    menu["Price(IncTax)"] = menu["Price"].apply(calc_tax_details,args=(0.1,))
    return menu

def main():
    config_file = read_json(sys.argv[1])
    supermarket_products = read_csv(config_file["supermarket_products_path"])
    menu = read_csv(config_file["menu_path"])
    fare_details_df = get_cost_details(supermarket_products, menu)
    display_fare_details(fare_details_df)

main()