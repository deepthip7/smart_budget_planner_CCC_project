# cli_version.py
# Run this file to test the Knapsack logic in the terminal (no GUI needed)

from knapsack import knapsack, print_dp_table
from items_data import SAMPLE_ITEMS

def run_cli():
    print("=" * 60)
    print("   💰 Smart Budget Planner — CLI Version")
    print("   Dynamic Programming | 0/1 Knapsack")
    print("=" * 60)

    # Show available items
    print("\n📦 Available Items:")
    print(f"{'#':<4} {'Name':<20} {'Price (₹)':>10} {'Value':>8}")
    print("-" * 46)
    for i, item in enumerate(SAMPLE_ITEMS, 1):
        print(f"{i:<4} {item['name']:<20} {item['price']:>10,} {item['value']:>8}")

    # Get budget input
    print()
    try:
        budget = int(input("Enter your budget (₹): "))
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return

    # Run DP
    max_value, selected, dp_table = knapsack(budget, SAMPLE_ITEMS)

    # Print DP Table (only if budget <= 20 to keep it readable)
    if budget <= 20000:
        print_dp_table(dp_table, SAMPLE_ITEMS, min(budget, 20))
    else:
        print("\n(DP table too large to display — budget > 20,000)")

    # Show results
    print("\n" + "=" * 60)
    print("✅ BEST ITEMS TO BUY:")
    print("=" * 60)

    if not selected:
        print("😕 No items fit within your budget.")
        return

    total_spent = 0
    for i, item in enumerate(selected, 1):
        print(f"  {i}. {item['name']:<20} ₹{item['price']:>8,}   ⭐ {item['value']} pts")
        total_spent += item['price']

    print("-" * 60)
    print(f"  {'Total Spent':<20} ₹{total_spent:>8,}")
    print(f"  {'Budget Remaining':<20} ₹{budget - total_spent:>8,}")
    print(f"  {'Total Value Score':<20} {max_value:>9} pts")
    print("=" * 60)


if __name__ == "__main__":
    run_cli()