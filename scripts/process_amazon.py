import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def clean_currency(value):
    if pd.isna(value): return 0.0
    # Remove ₹ and comma
    val = str(value).replace('₹', '').replace(',', '')
    try:
        return float(val)
    except:
        return 0.0

def process():
    print("Reading amazon.csv...")
    df_amazon = pd.read_csv('data/amazon.csv')
    
    # 1. Basic Cleaning
    df_amazon['unit_price'] = df_amazon['discounted_price'].apply(clean_currency)
    df_amazon['old_price'] = df_amazon['actual_price'].apply(clean_currency)
    
    # Filter out 0 price items
    df_amazon = df_amazon[df_amazon['unit_price'] > 0].copy()
    
    # 2. Extract Category / Subcategory
    # Format: "Computers&Accessories|Accessories&Peripherals|..."
    def split_cat(cat_str):
        parts = str(cat_str).split('|')
        main = parts[0] if len(parts) > 0 else 'Other'
        sub = parts[1] if len(parts) > 1 else 'General'
        return main, sub
    
    cats = df_amazon['category'].apply(split_cat)
    df_amazon['category'] = [c[0] for c in cats]
    df_amazon['subcategory'] = [c[1] for c in cats]
    
    print(f"Loaded {len(df_amazon)} real products.")

    # 3. Generate Transactions (Orders)
    num_orders = 5000
    countries = ['USA', 'UK', 'India', 'Germany', 'France', 'Canada', 'Australia', 'Brazil', 'Japan', 'Sweden']
    channels = ['Web', 'Mobile App', 'Marketplace', 'Retail Store']
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days

    orders = []
    
    print(f"Generating {num_orders} synthetic transactions...")
    for i in range(num_orders):
        # Pick a random product
        product = df_amazon.sample(n=1).iloc[0]
        
        # Random Date
        rand_days = random.randint(0, date_range)
        o_date = start_date + timedelta(days=rand_days)
        
        # Random Order Logic
        order_id = 10000 + i
        cust_id = random.randint(1001, 2600)
        country = random.choices(countries, weights=[20, 10, 25, 15, 10, 5, 5, 10, 5, 5])[0]
        city = f"City_{random.randint(1, 15)}" # Dummy city
        channel = random.choice(channels)
        qty = random.choices([1, 2, 3, 5], weights=[70, 20, 8, 2])[0]
        
        # Financials
        unit_p = product['unit_price']
        cost = unit_p * 0.7 # 30% margin baseline
        rev = unit_p * qty
        disc = (product['old_price'] - unit_p) * qty
        if disc < 0: disc = 0
        
        orders.append({
            'order_id': order_id,
            'order_date': o_date.strftime('%Y-%m-%d'),
            'customer_id': cust_id,
            'country': country,
            'city': city,
            'channel': channel,
            'product_id': product['product_id'],
            'category': product['category'],
            'subcategory': product['subcategory'],
            'unit_price': unit_p,
            'quantity': qty,
            'discount': disc,
            'revenue': rev,
            'cost': cost * qty
        })
        
    df_orders = pd.DataFrame(orders)
    df_orders.sort_values('order_date', inplace=True)
    
    # Save to data/orders.csv (Overwrite)
    df_orders.to_csv('data/orders.csv', index=False)
    print("Successfully updated data/orders.csv with Amazon product data!")

if __name__ == "__main__":
    process()
