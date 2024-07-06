import matplotlib.pyplot as plt
import pandas as pd
import numpy as np  
from calc_profit import product_profits


# Visualize the cost prices and selling price for all products across a state
def visualize_product_costprices(product_profits_df):
    products = product_profits_df["Product"]
    cost_prices = product_profits_df["CostPrice($)"]
    selling_prices = product_profits_df["SellingPrice($)Per1000Units"]
    product_indices = np.arange(len(products))
    plt.bar(product_indices - 0.2, cost_prices, 0.4, label = 'CostPrice($)') 
    plt.bar(product_indices + 0.2, selling_prices, 0.4, label = 'SellingPrice($)')
    plt.xlabel("Products") 
    plt.ylabel("Price") 
    plt.title("Product Profitability(1000units)")
    plt.xticks(product_indices,products) 
    plt.legend()
    plt.show()

def visualize():
    product_profits_df = product_profits()
    visualize_product_costprices(product_profits_df)

if __name__ == "__main__":
    visualize()
