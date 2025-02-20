import json

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_unique_dates(data):
    return list(data.keys())

def get_phone_numbers_for_date(data, date):
    return [entry["Phone_Number"] for entry in data[date]]

def check_missing_numbers(data, date, phone_numbers):
    existing_numbers = get_phone_numbers_for_date(data, date)
    missing_numbers = [num for num in phone_numbers if num not in existing_numbers]
    return missing_numbers

def main():
    file_path = 'processed_numbers.json'
    data = load_data(file_path)

    unique_dates = get_unique_dates(data)
    print("Unique dates available in the file:")
    for i, date in enumerate(unique_dates, 1):
        print(f"{i}. {date}")

    date_index = int(input("Select a date by entering its number: ")) - 1
    selected_date = unique_dates[date_index]

    phone_numbers_input = input("Enter phone numbers, separated by commas: ")
    phone_numbers = [num.strip() for num in phone_numbers_input.split(',')]
    phone_numbers = [num if num.startswith('+') else '+' + num for num in phone_numbers]

    missing_numbers = check_missing_numbers(data, selected_date, phone_numbers)
    print("Missing numbers:", ', '.join(missing_numbers))

if __name__ == "__main__":
    main()
