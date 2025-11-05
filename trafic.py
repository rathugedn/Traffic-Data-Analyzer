#Author: Devindi Nethmini Rathuge
#Date: 10/12/2024
#Student ID: 20232705(w2120417)

import csv
from pathlib import Path
from collections import defaultdict, Counter
import tkinter as tk

# Task A: Input Validation
"""
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
def validate_day_input():
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format DD: "))
            if not (1 <= day <= 31):
                print("Out of range - values must be in the range 1 and 31.")
                continue
            return day
        except ValueError:
            print("Integer required")
            
def validate_month_input():
    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if not (1 <= month <= 12):
                print("Out of range - values must be in the range 1 to 12.")
                continue
            return month
        except ValueError:
            print("Integer required")

def validate_year_input():
    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if not (2000 <= year <= 2024):
                print("Out of range - values must range from 2000 and 2024.")
                continue
            return year
        except ValueError:
            print("Integer required")

"""
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
def validate_continue_input():
    while True:
        choice = input("Do you want to select another data file for a different date? Y/N: ").strip().upper()
        if choice in ("Y", "N"):
            return choice
        else:
            print('Please enter "Y" or "N".')

# Task B: Processed Outcomes
"""
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
def process_csv_data(file_path):
    results = {
        "total_vehicles": 0,
        "total_trucks": 0,
        "total_electric_vehicles": 0,
        "two_wheeled_vehicles": 0,
        "busses_north": 0,
        "straight_path_vehicles": 0,
        "truck_percentage": 0,
        "bicycles_per_hour": 0,
        "over_speed_limit": 0,
        "vehicles_elm": 0,
        "vehicles_hanley": 0,
        "scooters_percentage_elm": 0,
        "peak_hour_vehicles": 0,
        "peak_hours": [],
        "rain_hours": 0,
    }

    hourly_traffic_elm = defaultdict(int)  # Traffic for Elm Avenue/Rabbit Road
    hourly_traffic_hanley = defaultdict(int)  # Traffic for Hanley Highway/Westway
    vehicle_count = Counter({"scooters_elm": 0, "bicycles": 0})

    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                results["total_vehicles"] += 1

                # Check for VehicleType
                if row.get("VehicleType", "").lower() == "truck":
                    results["total_trucks"] += 1

                # Check for electric hybrid status
                if row.get("elctricHybrid", "").lower() == "true":
                    results["total_electric_vehicles"] += 1

                # Check for two-wheeled vehicles
                if row.get("VehicleType", "").lower() in ["bicycle", "motorbike", "scooter"]:
                    results["two_wheeled_vehicles"] += 1

                # Buses traveling north on Elm Avenue/Rabbit Road
                if row.get("JunctionName", "").strip() == "Elm Avenue/Rabbit Road" and row.get("travel_Direction_out", "").strip() == "N" and row.get("VehicleType", "").strip().lower() == "bus":
                    results["busses_north"] += 1

                # Check for straight path vehicles
                if row.get("travel_Direction_in") == row.get("travel_Direction_out"):
                    results["straight_path_vehicles"] += 1

                # Over speed limit check
                try:
                    if int(row.get("VehicleSpeed", 0)) > int(row.get("JunctionSpeedLimit", 0)):
                        results["over_speed_limit"] += 1
                except ValueError:
                    pass  # Skip rows with invalid speed data

                # Elm Avenue/Rabbit Road vehicle count
                if row.get("JunctionName") == "Elm Avenue/Rabbit Road":
                    results["vehicles_elm"] += 1
                    if row.get("VehicleType", "").lower() == "scooter":
                        vehicle_count["scooters_elm"] += 1
                    hour = row.get("timeOfDay", "").split(":")[0]
                    hourly_traffic_elm[hour] += 1

                # Hanley Highway/Westway vehicle count
                if row.get("JunctionName") == "Hanley Highway/Westway":
                    results["vehicles_hanley"] += 1
                    hour = row.get("timeOfDay", "").split(":")[0]
                    hourly_traffic_hanley[hour] += 1

                # Rain condition check
                if row.get("Weather_Conditions", "").lower() == "rain":
                    results["rain_hours"] += 1

                # Bicycle count
                if row.get("VehicleType", "").lower() == "bicycle":
                    vehicle_count["bicycles"] += 1

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

    # Calculations
    if results["total_vehicles"] > 0:
        results["truck_percentage"] = round((results["total_trucks"] / results["total_vehicles"]) * 100)
    if results["vehicles_elm"] > 0:
        results["scooters_percentage_elm"] = round((vehicle_count["scooters_elm"] / results["vehicles_elm"]) * 100)
    if vehicle_count["bicycles"] > 0:
        results["bicycles_per_hour"] = round(vehicle_count["bicycles"] / 24)

    # Peak hour calculations
    results["peak_hour_vehicles"] = max(max(hourly_traffic_elm.values(), default=0), max(hourly_traffic_hanley.values(), default=0))
    results["peak_hours"] = [f"Between {hour}:00 and {int(hour)+1}:00" for hour, count in hourly_traffic_elm.items() if count == results["peak_hour_vehicles"]]
    results["peak_hours"] += [f"Between {hour}:00 and {int(hour)+1}:00" for hour, count in hourly_traffic_hanley.items() if count == results["peak_hour_vehicles"]]

    results["hourly_traffic_elm"] = hourly_traffic_elm
    results["hourly_traffic_hanley"] = hourly_traffic_hanley
    return results

# Display processed results
"""
    Displays the calculated outcomes in a clear and formatted way.
    """
def display_outcomes(results, file_name):
    print("\n***************************\n")
    print(f"Data file selected is {file_name}")
    print("\n***************************\n")
    print("The total number of vehicles recorded for this date is", results["total_vehicles"])
    print("The total number of trucks recorded for this date is", results["total_trucks"])
    print("The total number of electric vehicles for this date is", results["total_electric_vehicles"])
    print("The total number of two-wheeled vehicles for this date is", results["two_wheeled_vehicles"])
    print("The total number of buses leaving Elm Avenue/Rabbit Road heading North is", results["busses_north"])
    print("The total number of vehicles passing through junctions not turning left or right is", results["straight_path_vehicles"])
    print("The percentage of total vehicles recorded that are trucks for this date is", results["truck_percentage"], "%")
    print("The average number of bikes per hour for this date is", results["bicycles_per_hour"])
    print(f" \n")
    print("The total number of vehicles recorded that are over the speed limit for this date is", results["over_speed_limit"])
    print("The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is", results["vehicles_elm"])
    print("The total number of vehicles recorded through Hanley Highway/Westway junction is", results["vehicles_hanley"])
    print(f"{results['scooters_percentage_elm']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
    print(f" \n")
    print("The highest number of vehicles in an hour on Hanley Highway/Westway is", results["peak_hour_vehicles"])
    print("The most vehicles through Hanley Highway/Westway were recorded between", ", ".join(results["peak_hours"]))
    print("The number of hours of rain for this date is", results["rain_hours"])

# Task C: Save results to Text File
def save_results_to_file(results):
    with open("results.txt", mode="a") as file:
        file.write("The total number of vehicles recorded for this date is " + str(results["total_vehicles"]) + "\n")
        file.write("The total number of trucks recorded for this date is " + str(results["total_trucks"]) + "\n")
        file.write("The total number of electric vehicles for this date is " + str(results["total_electric_vehicles"]) + "\n")
        file.write("The total number of two-wheeled vehicles for this date is " + str(results["two_wheeled_vehicles"]) + "\n")
        file.write("The total number of buses leaving Elm Avenue/Rabbit Road heading North is " + str(results["busses_north"]) + "\n")
        file.write("The total number of vehicles passing through junctions not turning left or right is " + str(results["straight_path_vehicles"]) + "\n")
        file.write("The percentage of total vehicles recorded that are trucks for this date is " + str(results["truck_percentage"]) + "%\n")
        file.write("The average number of bikes per hour for this date is " + str(results["bicycles_per_hour"]) + "\n")
        file.write("The total number of vehicles recorded that are over the speed limit for this date is " + str(results["over_speed_limit"]) + "\n")
        file.write("The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is " + str(results["vehicles_elm"]) + "\n")
        file.write("The total number of vehicles recorded through Hanley Highway/Westway junction is " + str(results["vehicles_hanley"]) + "\n")
        file.write(str(results["scooters_percentage_elm"]) + "% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n")
        file.write("The highest number of vehicles in an hour on Hanley Highway/Westway is " + str(results["peak_hour_vehicles"]) + "\n")
        file.write("The most vehicles through Hanley Highway/Westway were recorded between " + ", ".join(results["peak_hours"]) + "\n")
        file.write("The number of hours of rain for this date is " + str(results["rain_hours"]) + "\n")
        file.write("*******************\n")

# Task D: Histogram Display
"""
        Initializes the histogram application with the traffic data and selected date.
        """
class HistogramApp:
    def __init__(self, hourly_traffic_elm, hourly_traffic_hanley, date):
        self.hourly_traffic_elm = hourly_traffic_elm
        self.hourly_traffic_hanley = hourly_traffic_hanley
        self.date = date
        self.root = tk.Tk()
        self.root.title(f"Histogram")

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        canvas = tk.Canvas(self.root, width=1600, height=800, bg='white')
        canvas.pack()

        all_hours = sorted(set(self.hourly_traffic_elm.keys()).union(self.hourly_traffic_hanley.keys()))
        max_count = max(max(self.hourly_traffic_elm.values(), default=0), max(self.hourly_traffic_hanley.values(), default=0))

        bar_width = 20
        spacing = 10
        x_offset = 50

        for i, hour in enumerate(all_hours):
            count_elm = self.hourly_traffic_elm.get(hour, 0)
            count_hanley = self.hourly_traffic_hanley.get(hour, 0)
            height_elm = (count_elm / max_count) * 300
            height_hanley = (count_hanley / max_count) * 300

            # Display the graph name
            canvas.create_text(80, 30, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", font=("Arial", 16, "bold"), fill="black", anchor="w")

            # Elm Avenue/Rabbit Road bar
            x1 = x_offset + i * (2 * bar_width + spacing)
            canvas.create_rectangle(x1, 350 - height_elm, x1 + bar_width, 350, fill='lightgreen')

            # Hanley Highway/Westway bar
            x2 = x1 + bar_width + 5
            canvas.create_rectangle(x2, 350 - height_hanley, x2 + bar_width, 350, fill='lightcoral')

            # Hour label at the center of the two bars
            label_x = x1 + bar_width + (x2 - (x1 + bar_width)) // 2
            canvas.create_text(label_x, 360, text=hour, font=("Arial", 10), fill="black")

            # Vehicle count above each bar
            canvas.create_text(x1 + bar_width / 2, 350 - height_elm - 10, text=str(count_elm), font=("Arial", 10), fill="lightgreen")
            canvas.create_text(x2 + bar_width / 2, 350 - height_hanley - 10, text=str(count_hanley), font=("Arial", 10), fill="lightcoral")

        # Legend
        canvas.create_rectangle(50, 50, 70, 70, fill="lightgreen")
        canvas.create_text(80, 60, text="Elm Avenue/Rabbit Road", anchor="w")

        canvas.create_rectangle(50, 80, 70, 100, fill="lightcoral")
        canvas.create_text(80, 90, text="Hanley Highway/Westway", anchor="w")

        canvas.create_text(800, 400, text="Hours 00:00 to 24:00", font=("Arial", 14), fill="black", anchor="center")
        self.root.mainloop()

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    """
        Initializes the application for processing multiple CSV files.
        """
    def __init__(self):
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        results = process_csv_data(file_path)
        if results:
            return results
        return None

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        while True:
            day = validate_day_input()
            month = validate_month_input()
            year = validate_year_input()

            file_name = f"traffic_data{day:02}{month:02}{year}.csv"
            print(f"Processing file: {file_name}...")

            results = self.load_csv_file(file_name)

            if results:
                display_outcomes(results, file_name)
                HistogramApp(results["hourly_traffic_elm"], results["hourly_traffic_hanley"], f"{day}-{month}-{year}").draw_histogram()

            continue_choice = validate_continue_input()
            if continue_choice == "N":
                break

if __name__ == "__main__":
    app = MultiCSVProcessor()
    app.handle_user_interaction()

# if you have been contracted to do this assignment please do not remove this line
