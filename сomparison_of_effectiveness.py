import csv
from BTrees.OOBTree import OOBTree
import timeit
import random

def load_data(filepath):
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        items = []
        for row in reader:
            items.append({
                'ID': int(row['ID']),
                'Name': row['Name'],
                'Category': row['Category'],
                'Price': float(row['Price'])
            })
        return items

def build_price_tree(items):
    price_tree = OOBTree()
    for item in items:
        price = item['Price']
        if price in price_tree:
            price_tree[price].append(item)
        else:
            price_tree[price] = [item]
    return price_tree

def build_dict(items):
    dct = {}
    for item in items:
        dct[item['ID']] = item
    return dct

def range_query_tree(price_tree, min_price, max_price):
    result = []
    for _, item_list in price_tree.items(min_price, max_price):
        result.extend(item_list)
    return result

def range_query_dict(dct, min_price, max_price):
    return [item for item in dct.values() if min_price <= item['Price'] <= max_price]

def main():
    filepath = 'generated_items_data.csv' 
    items = load_data(filepath)

    price_tree = build_price_tree(items)
    item_dict = build_dict(items)

    prices = [item['Price'] for item in items]
    min_price = min(prices)
    max_price = max(prices)
    price_ranges = [
        (p, min(p + 10, max_price)) for p in random.choices(prices, k=100)
    ]

    def test_tree():
        for min_p, max_p in price_ranges:
            range_query_tree(price_tree, min_p, max_p)

    tree_time = timeit.timeit(test_tree, number=1)

    def test_dict():
        for min_p, max_p in price_ranges:
            range_query_dict(item_dict, min_p, max_p)

    dict_time = timeit.timeit(test_dict, number=1)

    print("Загальний час виконання 100 діапазонних запитів:")
    print(f"OOBTree: {tree_time:.6f} секунд")
    print(f"dict:    {dict_time:.6f} секунд")

if __name__ == "__main__":
    main()