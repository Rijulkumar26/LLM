import random

# Sample data
sample_products = [
    {
        "name": "Floral Skirt",
        "price": {"Amazon": 39, "Ebay": 39, "Walmart": 29},
        "size": {"Amazon": ["S", "L"], "Ebay": ["M"], "Walmart": ["L", "M"]},
        "in_stock": {"Amazon": True, "Ebay": True, "Walmart": True},
        "PromoDiscount": {"Amazon": {"SAVE10": 10, "WELCOME20": 20}, "Ebay": {"SAVE10": 10, "WELCOME20": 20}, "Walmart": {"SAVE10": 10, "WELCOME20": 20}},
        "shoplocation": "Delhi"
    },
    {
        "name": "Casual Denim Jacket",
        "price": {"Amazon": 80, "Ebay": 75, "Walmart": 78},
        "size": {"Amazon": ["M", "L"], "Ebay": ["S", "M"], "Walmart": ["M", "XL"]},
        "in_stock": {"Amazon": True, "Ebay": True, "Walmart": False},
        "PromoDiscount": {"Amazon": {"SAVE10": 10, "WELCOME20": 20}, "Ebay": {"SAVE10": 10, "WELCOME20": 20}, "Walmart": {"SAVE10": 10, "WELCOME20": 20}},
        "shoplocation": "Delhi"
    },
    {
        "name": "White Sneakers",
        "price": {"Amazon": 65, "Ebay": 60, "Walmart": 70},
        "size": {"Amazon": ["XL"], "Ebay": ["S", "M", "L"], "Walmart": ["M", "L"]},
        "in_stock": {"Amazon": False, "Ebay": True, "Walmart": True},
        "PromoDiscount": {"Amazon": {"SAVE10": 10, "WELCOME20": 20}, "Ebay": {"SAVE10": 10, "WELCOME20": 20}, "Walmart": {"SAVE10": 10, "WELCOME20": 20}},
        "shoplocation": "Delhi"
    },
    {
        "name": "Striped Cotton T-Shirt",
        "price": {"Amazon": 25, "Ebay": 22, "Walmart": 24},
        "size": {"Amazon": ["S", "M", "L"], "Ebay": ["S", "M"], "Walmart": ["M", "L", "XL"]},
        "in_stock": {"Amazon": True, "Ebay": False, "Walmart": True},
        "PromoDiscount": {"Amazon": {"SAVE10": 10, "WELCOME20": 20}, "Ebay": {"SAVE10": 10, "WELCOME20": 20}, "Walmart": {"SAVE10": 10, "WELCOME20": 20}},
        "shoplocation": "Delhi"
    },
]

def search_products(query):
    """Search for products based on query keywords, ensuring proper product matching."""
    query = query.lower()
    relevant_keywords = query.split()

    matched_products = []
    attribute_query = None

    # Identify if user is asking for price, stock, size, etc.
    if "cost" in relevant_keywords or "price" in relevant_keywords:
        attribute_query = "price"
    elif "stock" in relevant_keywords or "availability" in relevant_keywords:
        attribute_query = "in_stock"
    elif "size" in relevant_keywords:
        attribute_query = "size"

    # Identify if a product name is in the query
    for product in sample_products:
        product_name = product["name"].lower()

        # Prioritize exact matches
        if product_name in query:
            matched_products.append(product)

    # If no exact match, do partial word match
    if not matched_products:
        for product in sample_products:
            product_name = product["name"].lower()
            if any(word in product_name for word in relevant_keywords):
                matched_products.append(product)

    # If product found, return requested attribute
    if matched_products:
        response = []
        for product in matched_products:
            if attribute_query:
                for store, value in product[attribute_query].items():
                    if store.lower() in relevant_keywords:  # Ensure store matches
                        response.append({
                            "product": product["name"],
                            "store": store,
                            attribute_query: value
                        })
                return response if response else [{"message": "Store not found for this product."}]
        
        return matched_products

    return [{"message": "No matching products found."}]


def estimate_shipping(user_location,query):
    """Mock function to calculate shipping costs based on a request."""
    matched_products = search_products(query)
    if matched_products and isinstance(matched_products, list) and "message" not in matched_products[0]:
        location = matched_products[0]
    if user_location.lower() == "bangalore" and location["shoplocation"].lower() == "delhi":
        return {"estimated_days": 4, "cost": random.choice([5, 10, 15]), "feasible": True}
    else:
        return {"estimated_days": random.randint(2, 7), "cost": random.choice([5, 10, 15]), "feasible": True}

def check_discount(query, promo_code=None):
    """Mock function to validate and apply discounts."""
    valid_discounts = {"SAVE10": 10, "WELCOME20": 20}
    if promo_code and promo_code in valid_discounts:
        return {"discount_applied": valid_discounts[promo_code], "message": f"Promo code {promo_code} applied successfully!"}
    return {"discount_applied": 0, "message": "No valid promo code applied."}

def compare_prices(query):
    """Compare prices across platforms for a specific product."""
    matched_products = search_products(query)
    if matched_products and isinstance(matched_products, list) and "message" not in matched_products[0]:
        product = matched_products[0]
        return {
            "product": product["name"],
            "prices": product["price"]
        }
    return {"message": "Product not found."}

def get_return_policy(query):
    """Mock function to return return policies of e-commerce stores."""
    return_policies = {
        "Amazon": "Returns within 30 days with free shipping.",
        "Ebay": "Returns within 15 days, shipping fee applicable.",
        "Walmart": "No returns allowed on discounted items.",
    }
    return {"return_policy": random.choice(list(return_policies.values()))}