#Calculated Price Inclusive of taxes for each product based on the state list
import pandas as pd
import sys,json

def read_json(json_path):
    with open(json_path,"r") as file:
        file_paths = json.load(file)
    return file_paths

def read_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df

def display_fare_details(menu_df_list):
    menu_df_combined = pd.concat(menu_df_list).reset_index(drop=True)
    print(menu_df_combined)

def calc_cost_details(row,super_market_df,menu):
    min_rate = super_market_df[super_market_df["Product"] == row["Product"]]["min"].values[0]
    menu.at[row.name,"MinimumRate"] =  min_rate
    return row["Quantity"] * min_rate

def calc_grocery_state_tax(state_tax_df,state):
    tax = state_tax_df.query("State == @state")["Tax(%)"].iat[0]
    return tax

def calc_tax_details(row,tax_data,menu,state):
    menu.at[row.name,"Tax(%)"] = tax_data
    menu.at[row.name,"State"] = state
    return row["Price"]*tax_data/100 + row["Price"]

def get_cost_details(supermarket_products, menu,grocery_tax,state):
    supermarket_products["min"] = supermarket_products[["SevenEleven($)","Walmart($)","Tesco($)"]].min(axis=1)
    menu["Price"] = menu.apply(calc_cost_details,args=(supermarket_products,menu),axis=1)
    menu["Price(IncTax)"] = menu.apply(calc_tax_details,args=(grocery_tax,menu,state),axis=1)
    return menu

def extract_csv_contents(config_file):
    supermarket_products = read_csv(config_file["supermarket_products_path"])
    state_taxes = read_csv(config_file["state_taxes_path"])
    menu = read_csv(config_file["menu_path"])
    csv_data = {
        "supermarket_data":supermarket_products,
        "menu_data" : menu,
        "tax_data":state_taxes
    }
    return csv_data
#User Input: python3 main.py config.json state_list
def main():
    menu_df_list = []
    config_file  = read_json("config.json")
    csv_data = extract_csv_contents(config_file)
    states = csv_data["tax_data"]["State"].unique()
    for state in  states:
        grocery_tax = calc_grocery_state_tax(csv_data["tax_data"],state)
        menu_df = get_cost_details(csv_data["supermarket_data"],
        csv_data["menu_data"],grocery_tax,state)
        menu_df_list.append(menu_df.copy())
    display_fare_details(menu_df_list)

main()