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
    transportation_charges = math.ceil(row["Quantity"]/1000) * transport_charges
    columns_dict = {
        "PriceIncTransportation($)":transportation_charges
    }
    return pd.Series(columns_dict)

def calc_discount(row,discount):
    product_index = discount[discount["Product"]==row["Product"]].index
    minimum_quantity = discount.at[product_index[0], "MinimumQuantity"]
    discount_percentage = discount.at[product_index[0], "Discount(%)"]
    discount_value = row["Cost($)"]  if row["Quantity"] < minimum_quantity else row["Cost($)"] - discount_percentage/100 * row["Cost($)"] 
    columns_dict = {
        "Discount(%)":discount_percentage,
        "DiscountedPrice($)":discount_value
    }
    return pd.Series(columns_dict)

def calc_total_cost(row):
    columns_dict = {
        "TotalCost": row["DiscountedPrice($)"]+row["PriceIncTransportation($)"]
    }
    return pd.Series(columns_dict)

def calc_minimum_total_cost(menu_charges_df):
    menu_charges_df.reset_index(drop=True)
    menu_total_cost_df = menu_charges_df.groupby("Product").min()
    return menu_total_cost_df.reset_index()

#TotalCost =  (((Price*Quantity) + Tax ) - discount_value) + PriceIncTransportation
def get_cost_details(csv_data):
    products_menu_df = pd.merge(csv_data["products_data"],csv_data["menu_data"],on=["Product"],how="outer")
    menu_taxes_df = pd.merge(products_menu_df,csv_data["tax_data"],on=["Product","State"],how="left").fillna(0)
    menu_taxes_df["Cost($)"] = menu_taxes_df.apply(calc_cost_details,axis=1)
    menu_charges_df = pd.merge(menu_taxes_df,csv_data["transportation_data"],on=["State"],how="left")
    menu_charges_df["PriceIncTransportation($)"] = menu_charges_df.apply(calc_transportation_charges,args=(csv_data["transportation_data"],),axis=1)
    menu_charges_df[["Discount(%)","DiscountedPrice($)"]] = menu_charges_df.apply(calc_discount,args=(csv_data["discount_data"],),axis=1)
    menu_charges_df["TotalCost($)"] = menu_charges_df.apply(calc_total_cost,axis=1)
    menu_charges_df = menu_charges_df.drop(menu_charges_df[menu_charges_df["Quantity"]==0].index)
    return calc_minimum_total_cost(menu_charges_df)

def extract_csv_contents(config):
    supermarket_products = read_csv(config["supermarket_products_path"])
    menu = read_csv(config["menu_path"])
    state_taxes = read_csv(config["state_taxes_path"])
    transportation_charges = read_csv(config["transportation_charges_path"])
    discount_percentage = read_csv(config["bulk_discount_path"])
    csv_data = {
        "products_data":supermarket_products,
        "menu_data":menu,
        "tax_data":state_taxes,
         "transportation_data":transportation_charges,
         "discount_data":discount_percentage

    }
    return csv_data

def main():
    config = read_json(sys.argv[1])
    csv_data = extract_csv_contents(config)
    least_prod_cost_df = get_cost_details(csv_data)
    display_df(least_prod_cost_df)

main()