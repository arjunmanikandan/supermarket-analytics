import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_bar_labels(cost_prices,selling_prices,bar_width):
    for i, (cost_price, sell_price) in enumerate(zip(cost_prices, selling_prices)):
        plt.text(i - bar_width/2, cost_price, f"${cost_price}", ha='center', va='bottom')
        plt.text(i + bar_width/2, sell_price, f"${sell_price}", ha='center', va='bottom')

#Renaming Individual x labels
def restructure_xticks(products):
    products_count = {}
    list(map(lambda product: products_count.update({product: products_count.get(product, 0) + 1}), products))
    products_count_labels = [f"{product}\nWeek{i}" for product, count in products_count.items() for i in range(1, count + 1)]
    return products_count_labels

def visualize_df(product_profits_df):
    product_indices,bar_width  = np.arange(len(product_profits_df["Product"])),0.4
    products_count_labels = restructure_xticks(product_profits_df["Product"])
    cost_prices = product_profits_df["CostPrice($)"]
    selling_prices = product_profits_df["SellingPrice($)Per1000Units"]
    create_bar_labels(cost_prices,selling_prices,bar_width)
    plt.bar(product_indices - bar_width/2, cost_prices, bar_width, label='Cost Price')
    plt.bar(product_indices + bar_width/2, selling_prices, bar_width, label='Selling Price')
    plt.title("Product Profitability (1000 units)")    
    plt.xlabel("Products")
    plt.ylabel("Price ($)")
    plt.xticks(product_indices,products_count_labels)
    plt.ylim(0, max(max(cost_prices), max(selling_prices)) + 5000)
    plt.tight_layout()
    plt.legend()
    plt.show()