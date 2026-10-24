"""
Dairy Co-op Payment Calculator
------------------------------
Farmer enters their name and litres supplied.
Tool shows total owed at current buying price.

Usage:
    python dairy_calculator.py

Config:
    Edit the value in price.txt to update the weekly rate.
"""

def get_current_price() -> float:
    """Read current price from price.txt, fall back to default."""
    try:
        with open("price.txt", "r") as f:
            return float(f.read().strip())
    except FileNotFoundError:
        return 55.0  # Default: KES 55 per litre
    except ValueError:
        print("⚠️ Warning: Invalid data in price.txt. Using default.")
        return 55.0


def calculate_payment(litres: float, price_per_litre: float) -> float:
    """Calculate total payment owed."""
    return litres * price_per_litre


def run() -> None:
    """Run the main CLI interface."""
    print("Kiambu Dairy Co-op Payment Calculator")
    print("--------------------------------------")
    
    price = get_current_price()
    print(f"Current buying price: KES {price:.2f} per litre\n")

    name = input("Farmer name: ").strip()
    if not name:
        print("❌ Error: Name is required.")
        return

    try:
        litres = float(input("Litres supplied today: "))
        if litres <= 0:
            print("❌ Error: Litres must be greater than zero.")
            return
    except ValueError:
        print("❌ Error: Please enter a valid number for litres.")
        return

    total = calculate_payment(litres, price)

    print("\n--- Receipt ---")
    print(f"Farmer : {name}")
    print(f"Litres : {litres} L")
    print(f"Price  : KES {price:.2f}/L")
    print(f"Total  : KES {total:,.2f}")
    print("---------------")


if __name__ == "__main__":
    run()