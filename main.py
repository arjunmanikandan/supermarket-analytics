import pandas as pd
import sys,json

def read_json(json_path):
    with open(json_path,"r") as file:
        file_paths = json.load(file)
    return file_paths

def read_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df

def display_df(menu_df):
    print(menu_df)

def calc_cost_details(row,supermarket_products):
    min_idx = supermarket_products[supermarket_products["Product"] == row["Product"]]["Price($)"].idxmin()
    columns_dict = {
        "Store":supermarket_products.at[min_idx,"Store"],
         "State":supermarket_products.at[min_idx,"State"],
         "MinimumRate($)":supermarket_products.at[min_idx,"Price($)"]

    }
    return pd.Series(columns_dict)

def calc_tax_details(row):
    product_price = row["MinimumRate($)"]*row["Quantity"]

    columns_dict = {
        "Price(IncTax)($)": product_price*row["Tax(%)"]/100 + product_price
    }
    return pd.Series(columns_dict)
    
def get_cost_details(supermarket_products, menu,taxes):
    menu[["Store","State","MinimumRate($)"]] = menu.apply(calc_cost_details,args=(supermarket_products,),axis=1)
    menu_taxes = pd.merge(menu,taxes,on=["State","Product"],how="left")
    menu_taxes.fillna({"Tax(%)":0}, inplace=True)
    menu_taxes["Price(IncTax)($)"] =  menu_taxes.apply(calc_tax_details,axis=1)
    return menu_taxes

def extract_csv_contents(config):
    supermarket_products = read_csv(config["supermarket_products_path"])
    menu = read_csv(config["menu_path"])
    state_taxes = read_csv(config["state_taxes_path"])
    csv_data = {
        "products_data":supermarket_products,
        "menu_data":menu,
        "tax_data":state_taxes
    }
    return csv_data

def main():
    config = read_json("config.json")
    csv_data = extract_csv_contents(config)
    menu_df = get_cost_details(csv_data["products_data"], csv_data["menu_data"],csv_data["tax_data"])
    display_df(menu_df)

main()