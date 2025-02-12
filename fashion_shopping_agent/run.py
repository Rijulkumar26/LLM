import json
from agent import process_user_query

def main():
    print("Welcome to the AI Shopping Assistant! Type 'exit' to quit.")
    user_location = input("Enter your location: ").strip()

    while True:
        user_query = input("\nAsk me something: ").strip()
        if user_query.lower() == "exit":
            print("Goodbye!")
            break

        # Get response and ensure it is a dictionary
        response_str = process_user_query(user_query,user_location, None)
        
        try:
            response = json.loads(response_str)  # Convert JSON string to dictionary
        except json.JSONDecodeError:
            print("\nError: Unexpected response format.")
            print(response_str)
            continue

        # Check if a product is found
        if "products" in response and response["products"]:
            print("\nFound the product! Do you have a promo code? (yes/no)")
            user_reply = input().strip().lower()

            if user_reply == "yes":
                promo_code = input("Enter promo code: ").strip()
                response_str = process_user_query(user_query,user_location, promo_code)

                try:
                    response = json.loads(response_str)  # Parse again after applying promo
                except json.JSONDecodeError:
                    print("\nError: Unexpected response format after promo.")
                    print(response_str)
                    continue

        print("\nAssistant Response:\n", json.dumps(response, indent=2))

if __name__ == "__main__":
    main()