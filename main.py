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

def calc_total(row,menu):
    total = menu.loc[row.name,"Quantity"]*(row["min"]) if row.name in menu.index else 0
    return total
 
def get_cost_details(supermarket_products, menu):
    supermarket_products["min"] = supermarket_products[["SevenEleven($)","Walmart($)","Tesco($)"]].min(axis=1)
    supermarket_products["price"] = supermarket_products.apply(calc_total,args=(menu,),axis=1)
    return pd.concat([supermarket_products,menu[["Quantity"]]],axis=1)

def main():
    config_file = read_json(sys.argv[1])
    supermarket_products = read_csv(config_file["supermarket_products_path"])
    menu = read_csv(config_file["menu_path"])
    fare_details_df = get_cost_details(supermarket_products, menu)
    display_fare_details(fare_details_df)

main()