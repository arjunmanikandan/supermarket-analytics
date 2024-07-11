import pandas as pd
import sys,json,math,os
from dotenv import load_dotenv
from calc_profit import product_profits
from visualize_data import visualize_df

def display_df(df_dict):
    print(df_dict["menu_cost_price_df"])
    print(df_dict["product_profit_df"])

def read_json(json_path):
    with open(json_path,"r") as file:
        file_paths = json.load(file)
    return file_paths

def read_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df

def get_df(menu_charges_df):
    menu_charges_df = menu_charges_df[['Product', 'Store', 'Location', 'Rate($)', 'Quantity','Price($)', 
        'Discount(%)','DiscountedPrice($)','Tax(%)','PriceIncTax($)','TransportationCharges($)', 
        'PriceIncTransportation($)','Week','CostPrice($)']]
    return menu_charges_df

def calc_cost_details(row):
    columns_dict = {
        "Price($)": row["Rate($)"]*row["Quantity"]
    }
    return pd.Series(columns_dict)

def calc_transportation_charges(row,charges):
    charges_index = charges[charges["Location"] == row["Location"]].index
    transport_charges = charges.at[charges_index[0],"TransportationCharges($)"]
    transportation_charges = math.ceil(row["Quantity"]/1000) * transport_charges
    columns_dict = {
        "PriceIncTransportation($)":transportation_charges
    }
    return pd.Series(columns_dict)

def calc_discount(row,discount):
    product_index = discount[discount["Product"]==row["Product"]].index
    minimum_quantity = discount.at[product_index[0], "MinimumQuantity"]
    discount_percentage = discount.at[product_index[0], "Discount(%)"]
    discount_value = row["Price($)"]  if row["Quantity"] < minimum_quantity else row["Price($)"] - discount_percentage/100 * row["Price($)"] 
    columns_dict = {
        "Discount(%)":discount_percentage,
        "DiscountedPrice($)":discount_value
    }
    return pd.Series(columns_dict)

def calc_total_cost(row):
    columns_dict = {
        "TotalCost": row["DiscountedPrice($)"]+row["Tax(%)"]/100*row["DiscountedPrice($)"]
    }
    return pd.Series(columns_dict)

def get_cost_details(csv_data):
    products_menu_df = pd.merge(csv_data["cost_prices_data"],csv_data["menu_data"],on=["Product"],how="outer")
    menu_taxes_df = pd.merge(products_menu_df,csv_data["tax_data"],on=["Product","Location"],how="left").fillna(0)
    menu_taxes_df["Price($)"] = menu_taxes_df.apply(calc_cost_details,axis=1)
    menu_charges_df = pd.merge(menu_taxes_df,csv_data["transportation_data"],on=["Location"],how="left")
    menu_charges_df["PriceIncTransportation($)"] = menu_charges_df.apply(calc_transportation_charges,args=(csv_data["transportation_data"],),axis=1)
    menu_charges_df[["Discount(%)","DiscountedPrice($)"]] = menu_charges_df.apply(calc_discount,args=(csv_data["discount_data"],),axis=1)
    menu_charges_df["PriceIncTax($)"] = menu_charges_df.apply(calc_total_cost,axis=1)
    menu_charges_df["CostPrice($)"] = menu_charges_df["PriceIncTax($)"] + menu_charges_df["PriceIncTransportation($)"]
    menu_charges_df = menu_charges_df.drop(menu_charges_df[menu_charges_df["Quantity"]==0].index)
    return menu_charges_df.reset_index(drop=True)

def extract_csv_contents(config):
    buying_prices = read_csv(config["buying_prices_path"])
    menu = read_csv(config["menu_path"])
    location_taxes = read_csv(config["location_taxes_path"])
    transportation_charges = read_csv(config["transportation_charges_path"])
    discount_percentage = read_csv(config["bulk_discount_path"])
    selling_prices = read_csv(config["selling_prices_path"])
    csv_data = {
        "cost_prices_data":buying_prices,
        "menu_data":menu,
        "tax_data":location_taxes,
         "transportation_data":transportation_charges,
         "discount_data":discount_percentage,
         "selling_prices_data":selling_prices,
    }
    return csv_data

def main():
    load_dotenv()
    config_path = os.getenv('CONFIG_PATH')
    config = read_json(config_path)
    csv_data = extract_csv_contents(config)
    least_prod_cost_df = get_cost_details(csv_data)
    menu_cost_price_df=get_df(least_prod_cost_df)
    product_profit_df = product_profits(csv_data,menu_cost_price_df,config)
    visualize_df(product_profit_df)
    df_dict ={
        "menu_cost_price_df":menu_cost_price_df,
        "product_profit_df":product_profit_df
    }
    return df_dict

if __name__ == "__main__":
    df_dict = main()
    display_df(df_dict)