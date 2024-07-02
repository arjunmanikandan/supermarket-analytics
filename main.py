import pandas as pd
import sys,json,math

def read_json(json_path):
    with open(json_path,"r") as file:
        file_paths = json.load(file)
    return file_paths

def read_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df

def display_df(menu_charges_df):
    print(menu_charges_df)

def extract_cheapest_prod_price(row,menu_taxes_df):
    minimum_price_idx = menu_taxes_df[menu_taxes_df["Product"]==row["Product"]]["Cost($)"].idxmin()
    return menu_taxes_df.loc[[minimum_price_idx]]

def calc_cost_details(row):
    price = row["Price($)"]*row["Quantity"]
    columns_dict = {
        "Cost($)": price + row["Tax(%)"]/100 * price
    }
    return pd.Series(columns_dict)

def calc_transportation_charges(row,charges):
    charges_index = charges[charges["State"] == row["State"]].index
    transport_charges = charges.at[charges_index[0],"TransportationCharges($)"]
    transportation_charges = transport_charges if row["Quantity"] <=1000 else math.ceil(row["Quantity"]/1000) * transport_charges
    columns_dict = {
        "Rate($)":transportation_charges
    }
    return pd.Series(columns_dict)

#The transportation charges listed in the CSV file are per 1000 units
def get_cost_details(supermarket_products,menu,taxes,charges):
    products_menu_df = pd.merge(supermarket_products,menu,on=["Product"],how="outer")
    menu_taxes_df = pd.merge(products_menu_df,taxes,on=["Product","State"],how="left").fillna(0)
    menu_taxes_df["Cost($)"] = menu_taxes_df.apply(calc_cost_details,axis=1)
    menu_dfs = menu.apply(extract_cheapest_prod_price,args=(menu_taxes_df,),axis=1)
    least_prod_cost_df = list(map(lambda df : df,menu_dfs))
    least_prod_cost_df = pd.concat(least_prod_cost_df,ignore_index=True)
    menu_charges_df = pd.merge(least_prod_cost_df,charges,on=["State"],how="left")
    menu_charges_df["Rate($)"] = menu_charges_df.apply(calc_transportation_charges,args=(charges,),axis=1)
    return menu_charges_df
    
def extract_csv_contents(config):
    supermarket_products = read_csv(config["supermarket_products_path"])
    menu = read_csv(config["menu_path"])
    state_taxes = read_csv(config["state_taxes_path"])
    transportation_charges = read_csv(config["transportation_charges_path"])
    csv_data = {
        "products_data":supermarket_products,
        "menu_data":menu,
        "tax_data":state_taxes,
         "transportation_data":transportation_charges
    }
    return csv_data

def main():
    config = read_json(sys.argv[1])
    csv_data = extract_csv_contents(config)
    least_prod_cost_df = get_cost_details(csv_data["products_data"], 
    csv_data["menu_data"],csv_data["tax_data"],csv_data["transportation_data"])
    display_df(least_prod_cost_df)

main()