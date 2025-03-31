from crewai import Crew, Process
from crewgemini.tasks import (
    attraction_task, weather_task, accommodation_task, transportation_task, schedule_task
)
from crewgemini.agents import (
    destination_agent, weather_agent, accommodation_agent, transportation_agent, schedule_builder_agent
)

# Create the Crew instance
crew = Crew(
    agents=[destination_agent, weather_agent, accommodation_agent, transportation_agent, schedule_builder_agent],
    tasks=[attraction_task, weather_task, accommodation_task, transportation_task, schedule_task],
    process=Process.sequential,
)

# Run AI-powered itinerary generation
def run_itinerary(origin, destination, num_days, date, budget, location_preference, amenities, accommodation_type):
    print(f"🛫 Generating itinerary for {origin} → {destination} on {date} for {num_days} days")

    result = crew.kickoff(inputs={
        'origin': origin, 
        'destination': destination, 
        'num_days': num_days, 
        'date': date,
        'budget': budget,
        'location_preference': location_preference, 
        'amenities': amenities, 
        'accommodation_type': accommodation_type
    })

    print("🚀 CrewAI Raw Output:", result)  # Debug output

    return result
