from crewai import Task 
from crewgemini.tools import tools
from crewgemini.agents import destination_agent, weather_agent, accommodation_agent, transportation_agent,schedule_builder_agent 


# Task 1: Find the best attractions
attraction_task = Task(
    name="Find Top Attractions",
    agent=destination_agent,
    description=(
        "Gather information on must-visit tourist attractions, cultural sites, "
        "and hidden gems in {destination}. Consider traveler preferences, "
        "seasonal activities, and local events."
    ),
    tools=[tools["search"]],
    expected_output="A list of top attractions with descriptions, ratings, and best times to visit."
)

# Task 2: Check Weather Forecast
weather_task = Task(
    name="Get Weather Forecast",
    agent=weather_agent,
    description=(
        "Retrieve real-time weather updates for {destination} on {date}. "
        "Provide temperature, precipitation chances, and weather advisories "
        "to help adjust travel plans."
    ),
    tools=[tools["search"]],
    expected_output="A detailed weather report with recommendations for travel adjustments."
)

# Task 3: Find Suitable Accommodations
accommodation_task = Task(
    name="Find Best Accommodations",
    agent=accommodation_agent,
    description=(
        "Search for the best {accommodation_type} in {destination} within a budget of {budget}. "
        "Prioritize location near {location_preference} and ensure it includes amenities: {amenities}. "
        "Provide a list of accommodations with price ranges, ratings, and key features."
    ),
    tools=[tools["search"]],
    expected_output="A list of recommended accommodations with price ranges, ratings, and amenities."
)

# Task 4: Plan Transportation Options
transportation_task = Task(
    name="Suggest Transportation Options",
    agent=transportation_agent,
    description=(
        "Provide the best transportation options for traveling from {origin} to {destination}, "
        "as well as commuting within {destination}. "
        "Include flights, trains, rental cars, and public transit recommendations based on budget and convenience."
    ),
    tools=[tools["maps"]],
    expected_output="A list of recommended transportation options from {origin} to {destination}, "
                    "along with estimated travel times, costs, and local commuting options."
)

# Task 5: Create Personalized Itinerary
schedule_task = Task(
    name="Create Personalized Travel Schedule",
    agent=schedule_builder_agent,
    description=(
        "Using the list of attractions found by the Destination Researcher, create a personalized {num_days}-day travel plan "
        "for {destination}. Include details like best visit times, transportation, meal breaks, and alternative plans for weather changes."
    ),
    tools=[tools["maps"], tools["search"]],
    expected_output="A structured day-by-day itinerary with attraction visits, travel routes, "
                    "meal breaks, and relaxation time optimized for efficiency."
)

# List of tasks
tasks = [attraction_task, weather_task, accommodation_task, transportation_task, schedule_task]