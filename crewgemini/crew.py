from crewai import Crew, Process
from crewgemini.tasks import attraction_task, weather_task, accommodation_task, transportation_task
from crewgemini.agents import destination_agent, weather_agent, accommodation_agent, transportation_agent

crew =  Crew(
    agents=[destination_agent, weather_agent, accommodation_agent, transportation_agent],
    tasks=[attraction_task, weather_task, accommodation_task, transportation_task],
    process=Process.sequential,
)


# Run AI-powered itinerary generation
def run_itinerary(origin, destination, date):
    return crew.kickoff(inputs={'origin': origin, 'destination': destination, 'date': date})
