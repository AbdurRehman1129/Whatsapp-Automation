import json
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data(file_name):
    """Load data from JSON file."""
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        return None

def get_dates(data):
    """Get all the dates from the JSON data."""
    return list(data.keys())

def get_unique_values(data, date):
    """Get unique OTP_Status values for a given date."""
    return list(set(entry["OTP_Status"] for entry in data[date]))

def filter_data(data, date, otp_status):
    """Filter data by date and OTP_Status."""
    return [entry for entry in data[date] if entry["OTP_Status"] == otp_status]

def main_menu(data):
    """Main menu to allow user to navigate and make choices repeatedly."""
    while True:
        dates = get_dates(data)
        print("\nAvailable dates:")
        for i, date in enumerate(dates, 1):
            print(f"{i}. {date}")

        date_choice = int(input("\nSelect a date by entering its number (or 0 to exit): ")) - 1
        if date_choice == -1:
            print("Exiting program. Goodbye!")
            break

        if date_choice < 0 or date_choice >= len(dates):
            print("Invalid choice. Please try again.")
            continue

        selected_date = dates[date_choice]
        unique_values = get_unique_values(data, selected_date)

        print(f"\nUnique OTP_Status values for {selected_date}:")
        for i, value in enumerate(unique_values, 1):
            print(f"{i}. {value}")

        value_choice = int(input("\nSelect a value by entering its number (or 0 to go back): ")) - 1
        if value_choice == -1:
            continue

        if value_choice < 0 or value_choice >= len(unique_values):
            print("Invalid choice. Please try again.")
            continue

        selected_value = unique_values[value_choice]
        filtered_data = filter_data(data, selected_date, selected_value)

        print(f"\nPhone numbers with OTP_Status '{selected_value}' on {selected_date}:")
        for entry in filtered_data:
            print(f"Phone Number: {entry['Phone_Number']}, Time: {entry['Time']}")

def main():
    file_name = "processed_numbers.json"
    data = load_data(file_name)

    if not data:
        return

    main_menu(data)

if __name__ == "__main__":
    clear_screen()
    main()
