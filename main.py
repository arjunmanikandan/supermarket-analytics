#Calculated Price Inclusive of taxes for each product based on the given state
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

def calc_grocery_state_tax(state_tax_df,state_name):
    tax = state_tax_df.query("State == @state_name")["Tax(%)"].iat[0]
    return tax

def calc_tax_details(price,tax_data):
    return price*tax_data + price

def get_cost_details(supermarket_products, menu,grocery_tax,tax_df):
    supermarket_products["min"] = supermarket_products[["SevenEleven($)","Walmart($)","Tesco($)"]].min(axis=1)
    menu["Price"] = menu.apply(calc_cost_details,args=(supermarket_products,menu),axis=1)
    menu["Price(IncTax)"] = menu["Price"].apply(calc_tax_details,args=(grocery_tax/100,))
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

#User Input: python3 main.py config.json Idaho
def main():
    config_file = read_json(sys.argv[1])
    state_name = sys.argv[2]
    csv_data = extract_csv_contents(config_file)
    grocery_tax = calc_grocery_state_tax(csv_data["tax_data"],state_name)
    fare_details_df = get_cost_details(csv_data["supermarket_data"],
    csv_data["menu_data"],grocery_tax,csv_data["tax_data"])
    display_fare_details(fare_details_df)

main()