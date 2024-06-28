import pandas as pd
import sys,json

def read_json(json_path):
    with open(json_path,"r") as file:
        file_paths = json.load(file)
    return file_paths

def read_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df

def display_df(least_prod_cost_df):
    print(pd.concat(least_prod_cost_df,ignore_index=True))

def extract_cheapest_prod_price(row,menu_taxes_df):
    minimum_price_idx = menu_taxes_df[menu_taxes_df["Product"]==row["Product"]]["TotalCost($)"].idxmin()
    return menu_taxes_df.loc[[minimum_price_idx]]

def calc_cost_details(row):
    price = row["Price($)"]*row["Quantity"]
    columns_dict = {
        "TotalCost($)": price + row["Tax(%)"]/100 * price
    }
    return pd.Series(columns_dict)
    
def get_cost_details(supermarket_products, menu,taxes):
    products_menu_df = pd.merge(supermarket_products,menu,on=["Product"],how="outer")
    menu_taxes_df = pd.merge(products_menu_df,taxes,on=["Product","State"],how="left").fillna(0)
    menu_taxes_df["TotalCost($)"] = menu_taxes_df.apply(calc_cost_details,axis=1)
    menu_dfs = menu.apply(extract_cheapest_prod_price,args=(menu_taxes_df,),axis=1)
    least_prod_cost_df = map(lambda df : df,menu_dfs)
    return list(least_prod_cost_df)

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
    config = read_json(sys.argv[1])
    csv_data = extract_csv_contents(config)
    least_prod_cost_df = get_cost_details(csv_data["products_data"], csv_data["menu_data"],csv_data["tax_data"])
    display_df(least_prod_cost_df)

main()