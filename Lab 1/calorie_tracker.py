
# Name: Swastik Saxena
# Project Title: Daily Calorie Tracker CLI

def get_float_input(prompt, default=None):
    """Helper function to safely get float input."""
    while True:
        try:
            val = input(prompt)
            if default is not None and not val:
                return default
            return float(val)
        except ValueError:
            print(" Invalid input. Please enter a numerical value.")

def main():
    """Main function to run the calorie tracker."""
    print("=" * 50)
    print("        \U0001F963 Daily Calorie Tracker CLI \U0001F963")
    print("=" * 50)
    
    meal_names = []
    calorie_amounts = []

    daily_limit = get_float_input("Enter your daily calorie limit (default 2000): ", 2000.0)

    num_meals = int(get_float_input("How many meals/items did you have today? "))
    
     
    for i in range(num_meals):
        print(f"\nMeal #{i+1}")
        meal_names.append(input("Enter meal name: "))
        calories = get_float_input("Enter calorie amount: ")
        calorie_amounts.append(calories)

    if not meal_names:
        print("\nNo meals were entered. Exiting Calorie Tracker.")
        return

     
    total_calories = sum(calorie_amounts) # Calculate total
    average_calories = total_calories / num_meals #  Calculate average

    if total_calories > daily_limit:
        warning = f" WARNING! Exceeded limit by: {total_calories - daily_limit:.2f} calories."
    else:
        warning = f" Success! Remaining until limit: {daily_limit - total_calories:.2f} calories."
    
    report = []
    report.append("\n" + "="*50)
    report.append("              \U0001F4C3 DAILY CALORIE REPORT \U0001F4C3")
    report.append("="*50)
    report.append(f"Daily Limit Set:\t{daily_limit:>10.2f} calories")
    report.append("-" * 50)
    report.append(f"{'Meal Name':<20}\t{'Calories':>10}")
    report.append("-" * 35)

    
    for name, calories in zip(meal_names, calorie_amounts):
        report.append(f"{name:<20}\t{calories:>10.2f}")

    
    report.append("-" * 35)
    report.append(f"{'Total:':<20}\t{total_calories:>10.2f}")
    report.append(f"{'Average:':<20}\t{average_calories:>10.2f}")
    report.append("=" * 50)
    report.append(warning)
    report.append("=" * 50 + "\n")

    final_report = "\n".join(report)
    print(final_report)

    if input("Save session log to file? (yes/no): ").lower() == 'yes':
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = f"calorie_log_{timestamp}.txt"
        
        try:
            with open(filename, "w") as file:
                file.write(f"*** DAILY CALORIE TRACKER SESSION LOG ***\n")
                file.write(f"Date/Time: {timestamp}\n")
                file.write(f"Daily Limit Set: {daily_limit:.2f}\n")
                file.write(f"Total Calories Consumed: {total_calories:.2f}\n")
                file.write(f"{warning}\n")
                file.write("-" * 40 + "\n")
                file.write(f"{'Meal Name':<20} | {'Calories':>10}\n")
                file.write("-" * 40 + "\n")
                for name, calories in zip(meal_names, calorie_amounts):
                    file.write(f"{name:<20} | {calories:>10.2f}\n")
            
            print(f"\n\U0001F4BE Session successfully saved to {filename}")
        except IOError:
            print(f"\n An error occurred while writing to {filename}.")

if __name__ == "__main__":
    main()