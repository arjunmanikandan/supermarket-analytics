#Identified the cheapest product cost for each store.
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
    
def identify_store_by_mincost(row,products_df):
    product_row = products_df[products_df['Product'] == row['Product']]
    min_value = product_row['min'].values[0]
    product_series = product_row[['SevenEleven($)', 'Walmart($)', 'Tesco($)']].idxmin(axis=1)
    store_name = product_series[product_series.index[0]] if row['MinimumRate'] == min_value else "NA"
    return store_name
    
def add_columns(row,supermarket_products):
    additional_colns = {
        "Price(IncTax)" : calc_tax_details(row["Price"],0.1),
        "Store" : identify_store_by_mincost(row,supermarket_products)
    }
    return pd.Series(additional_colns)

def get_cost_details(supermarket_products, menu):
    supermarket_products["min"] = supermarket_products[["SevenEleven($)","Walmart($)","Tesco($)"]].min(axis=1)
    menu["Price"] = menu.apply(calc_cost_details,args=(supermarket_products,menu),axis=1)
    menu[["Price(IncTax)","Store"]] = menu.apply(add_columns,args=(supermarket_products,),axis=1)
    return menu

def extract_csv_contents(config):
    supermarket_products = read_csv(config["supermarket_products_path"])
    menu = read_csv(config["menu_path"])
    csv_data = {
        "products_data":supermarket_products,
        "menu_data":menu
    }
    return csv_data

def main():
    config = read_json(sys.argv[1])
    csv_data = extract_csv_contents(config)
    fare_details_df = get_cost_details(csv_data["products_data"], csv_data["menu_data"])
    display_fare_details(fare_details_df)

main()