import datetime
from plant import Plant
from apis import Trefle
from apis import Weather


# Define a class for the Plant Care application.
class CoreFunctions:
  # Initialize the application with an empty list of plants.
  def __init__(self):
    self.plants = []
    self.current_date = datetime.date.today()
    self.city = "Lisbon"  # Default city

  # Function to get user's name and house location
  def get_user_info(self):
    self.username = input("Enter your name: ")
    self.city = input("Where do you live?: ")

  # Display a list of plants with their IDs
  def list_plants_with_ids(self):
    for i, plant in enumerate(self.plants):
      print(
        f"\n{i + 1}. {plant.name} ({plant.plant_type}) - Water every {plant.watering_frequency} days"
      )

  # Add a plant to the list
  def add_plant(self):
    name = input("\nEnter plant nickname: ")
    plant_type = input("Enter plant type: ")
    watering_frequency_over_20 = int(
      input("Enter watering frequency over 20 deg (in days): "))
    watering_frequency_under_20 = int(
      input("Enter watering frequency under 20 deg (in days): "))
    plant = Plant(name, plant_type, watering_frequency_over_20,
                  watering_frequency_under_20)
    self.plants.append(plant)
    print("\n#############################")
    print(f"Added plant: {name}")
    # Fetch and display plant information after adding the plant
    Trefle.get_plant_information(plant_type)
    print("#############################")

  # Delete a plant from the list
  def delete_plant(self):
    self.list_plants_with_ids()
    plant_id = input("\nEnter the ID of the plant you want to delete: ")
    if plant_id.isdigit():
      plant_id = int(plant_id) - 1
      if 0 <= plant_id < len(self.plants):
        plant = self.plants.pop(plant_id)
        print(f"\nDeleted plant: {plant.name}")
      else:
        print("Invalid plant ID.")
    else:
      print("Invalid input. Please enter a valid ID.")

  # Update the watering frequency of a plant
  def update_watering_frequency(self):
    self.list_plants_with_ids()
    plant_id = input("\nEnter the ID of the plant you want to update: ")
    if plant_id.isdigit():
      plant_id = int(plant_id) - 1
      if 0 <= plant_id < len(self.plants):
        new_frequency = int(
          input("Enter the new watering frequency (in days): "))
        plant = self.plants[plant_id]
        plant.watering_frequency = new_frequency
        print(
          f"Updated watering frequency for {plant.name} to {new_frequency} days"
        )
      else:
        print("Invalid plant ID.")
    else:
      print("Invalid input. Please enter a valid ID.")

  # Mark a plant as watered by updating its last_watered date
  def mark_as_watered(self):
    self.list_plants_with_ids()
    plant_id = input(
      "\nEnter the ID of the plant you want to mark as watered: ")
    if plant_id.isdigit():
      plant_id = int(plant_id) - 1
      if 0 <= plant_id < len(self.plants):
        plant = self.plants[plant_id]
        plant.last_watered = self.current_date
        print(f"Marked {plant.name} as watered")
      else:
        print("Invalid plant ID.")
    else:
      print("Invalid input. Please enter a valid ID.")

  # Check the watering schedule for all plants
  def check_watering_schedule(self):
    # Get the 5-day weather forecast for the user's city
    weather_forecast = Weather.get_weather_forecast(self.city)
    avg_temperature = weather_forecast['average']
    print(
      f"\nIn {self.city} the average maximum temperature will be {round(avg_temperature, 1)} degrees in the next five days. Your watering Schedule has been updated!"
    )
    print("\nWatering Schedule:")
    plants_by_days_left = {}
    for plant in self.plants:
      # Decide which watering frequency to use based on the average temperature
      if avg_temperature >= 20:
        watering_frequency = plant.watering_frequency_over_20
      else:
        watering_frequency = plant.watering_frequency_under_20

      days_since_last_watered = (datetime.date.today() -
                                 plant.last_watered).days
      days_until_next_watering = watering_frequency - days_since_last_watered
      if days_until_next_watering in plants_by_days_left:
        plants_by_days_left[days_until_next_watering].append(plant)
      else:
        plants_by_days_left[days_until_next_watering] = [plant]

    sorted_days_left = sorted(
      plants_by_days_left.keys())  # Moved this line here
    if sorted_days_left:
      nearest_day = sorted_days_left.pop(0)
      print(f"These plants need to be watered next, in {nearest_day} day(s):")
      for plant in plants_by_days_left[nearest_day]:
        print(f"1. {plant.name} ({plant.plant_type})")

      print("\nThese are the next Plants to be watered:")
      for days_left in sorted_days_left:
        for plant in plants_by_days_left[days_left]:
          print(f"{plant.name} ({plant.plant_type}) - in {days_left} days")

  # Update the current date by a certain number of days (positive for future, negative for past)
  def update_current_date(self, days):
    self.current_date += datetime.timedelta(days=days)
  
  def menu(self):
    while True:
      print("\nMenu:")
      print("1. Add Plant")
      print("2. Delete Plant")
      print("3. Update Watering Frequency")
      print("4. Mark Plant as Watered")
      print("5. Check Watering Schedule")
      print("6. DEMO - Jump to certain date")
      print("7. Exit")

      choice = input("Choose a menu number: ")

      if choice == "1":
        self.add_plant()
      elif choice == "2":
        self.delete_plant()
      elif choice == "3":
        self.update_watering_frequency()
      elif choice == "4":
        self.mark_as_watered()
      elif choice == "5":
        self.check_watering_schedule()
      elif choice == "6":
        self.check_watering_schedule()
      elif choice == "7":
        print("Goodbye!")
        break
      elif choice == "8":  # Dev function
        print(self.plants.json())
      else:
        print("Invalid choice. Please try again.")
 
import datetime

# Define a class for plants.
class Plant:
  # Initialize a plant with a name, type, watering frequency, and last watered date.
  def __init__(self, name, plant_type, watering_frequency_over_20, watering_frequency_under_20, last_watered=None):
    self.name = name
    self.plant_type = plant_type
    self.watering_frequency = watering_frequency_over_20
    self.watering_frequency_over_20 = watering_frequency_over_20
    self.watering_frequency_under_20 = watering_frequency_under_20
    self.last_watered = last_watered if last_watered else datetime.date.today()
    
    
import requests
from datetime import datetime


# Class containing all functionalities for the Trefle API, which can access specific plant information
class Trefle:
  global T_API_KEY
  T_API_KEY = '_ljWPEv9qFjPuM5KNTVDTR1r_Q9c6aeFe_7u8HcmgNk'

  # Function to fetch plant information from the Treffle API using the plant name
  @staticmethod
  def get_plant_information(plant_name):
    url = f'https://trefle.io/api/v1/plants/search?token={T_API_KEY}&q={plant_name}'
    # Send a GET request to the API
    search_response = requests.get(url)

    # Process the response
    if search_response.status_code == 200:
      search_data = search_response.json()
      if search_data['data']:
        # Extract the first plant data from the response, assuming it's the most relevant
        plant_info = search_data['data'][0]
        plant_self_link = f"https://trefle.io{plant_info['links']['plant']}?token={T_API_KEY}"
        # Send a GET request to fetch the detailed plant data
        plant_response = requests.get(plant_self_link)

        if plant_response.status_code == 200:
          plant_data = plant_response.json()
          family_common_name = plant_data['data'].get('family_common_name')
          scientific_name = plant_data['data'].get('scientific_name')
          observations = plant_data['data'].get('observations')
          # Print the plant information
          print(
            f"\nScientific name: {scientific_name if scientific_name is not None else 'Unknown'}"
          )
          print(
            f"Family: {family_common_name if family_common_name is not None else 'Unknown'}"
          )
          print(
            f"Observations: {observations if observations is not None else 'Unknown'}"
          )

        else:
          print(
            f"Error fetching detailed plant data: {plant_response.status_code}"
          )
      else:
        print(f"No information found for {plant_name}.")
    else:
      print(f"Error fetching plant data: {search_response.status_code}")


# Class containing all functionalities for the Weather API
class Weather:
  global W_API_KEY
  W_API_KEY = 'd3b82e6ee87d525aac2198fa19430391'

  @staticmethod
  def get_weather_forecast(city):
    # Construct the API request URL
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={W_API_KEY}"

    # Fetch the weather forecast data
    forecast_response = requests.get(url)
    
    # Process the response
    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        
        # Check if 'list' data exists
        if forecast_data.get('list'):
            # Dictionary to store each day's max temperatures
            daily_temperatures = {}

            for item in forecast_data['list']:
                # Convert the forecast time string to a datetime object
                forecast_time = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')

                # Use the date as the dictionary key
                date = forecast_time.date()

                # If the date is new, add an entry in the dictionary with a one-item list of max temperature
                if date not in daily_temperatures:
                    daily_temperatures[date] = [item['main']['temp_max']]

                # If the date exists, append the max temperature to the existing list
                else:
                    daily_temperatures[date].append(item['main']['temp_max'])

            # Calculate daily max temperatures
            daily_max_temps = {
                date: max(temps)
                for date, temps in daily_temperatures.items()
            }

            # Calculate the average of daily max temperatures
            average_max_temp = sum(daily_max_temps.values()) / len(daily_max_temps)

            return {
                "max": max(daily_max_temps.values()),
                "min": min(daily_max_temps.values()),
                "average": round(average_max_temp, 2)
            }
        else:
            print(f"No forecast data found for {city}.")
    else:
        print(f"Error fetching weather data: {forecast_response.status_code}")
       
from plant_care_app import CoreFunctions
from welcome import welcome_screen
import time

# Create an instance of the app and start it
if __name__ == "__main__":
  # Display the welcome screen and wait 1 second
  welcome_screen()
  time.sleep(1)
  
  # Display the menu and handle user input
  app = CoreFunctions()
  app.get_user_info()
  app.menu()
