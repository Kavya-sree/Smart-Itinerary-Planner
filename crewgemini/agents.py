import os
import litellm
from crewai import Agent, LLM
from crewgemini.tools import tools
from dotenv import load_dotenv 
load_dotenv()


from langchain_google_genai import ChatGoogleGenerativeAI

# Checking if the API key is set properly
if (not os.getenv("GOOGLE_API_KEY")):
    raise Exception("Please set GOOGLE_API_KEY.")

os.environ["LITELLM_PROVIDER"] = "google"

llm = LLM(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini/gemini-2.0-flash-lite",
)

# Define CrewAI Agents

# Destination Researcher
destination_agent = Agent(
    name="Destination Researcher",
    role="Find the best tourist attractions and activities in {destination}.",
    goal="Provide well-researched travel recommendations based on user preferences and weather conditions.",
    backstory="""You are an experienced travel researcher who has explored the world.
        You provide detailed travel guides, suggest must-visit attractions,
        and help travelers plan unforgettable experiences. 
        You work closely with weather forecasts
        to suggest the best activities based on climate.""",
    verbose=True,
    memory=True,
    tools=[tools["search"]],
    llm=llm,
    allow_delegation=True
)

# Weather Forecaster
weather_agent = Agent(
    name="Weather Forecaster",
    role="Provide accurate weather forecasts for {destination} to help plan suitable activities.",
    goal="Deliver precise weather forecasts to assist travelers in making informed decisions.",
    backstory=
        """You are an expert meteorologist who specializes in travel forecasting. 
        You analyze weather patterns, temperature, and precipitation levels 
        to guide travelers on the best times to visit locations. 
        You work closely with the Destination Researcher to ensure that
        suggested activities align with expected weather conditions.""",
    verbose=True,
    memory=True,
    tools=[tools["search"]],  
    llm=llm,
    allow_delegation=True
)

# Accommodation Specialist
accommodation_agent = Agent(
    name="Accommodation Specialist",
    role="Find the best hotels, resorts, hostels, or vacation rentals in {destination}.",
    goal="Find the most suitable accommodations based on user preferences, budget, and location",
    backstory=
        """You are a seasoned travel consultant who specializes in finding the best accomodations. 
        You analyze user preferences, budget, and location to recommend the best places to stay. 
        You work closely with the Destination Researcher and Transportation Specialist
        to ensure a seamless travel experience.""",
    verbose=True,
    memory=True,
    tools=[tools["search"]],
    llm=llm,
    allow_delegation=True
)


# Transportation Specialist
transportation_agent = Agent(
    role="Find the best transportation options for traveling from {origin} to {destination} and getting around the destination.",
    goal="Recommend the best transportation options for traveling from {origin} to {destination}, optimizing for cost, efficiency, and convenience.",
    backstory= """You are a travel logistics expert specializing in transportation. 
    You analyze flight options, train schedules, public transport routes, and rental cars 
    to suggest the most efficient and cost-effective travel methods. 
    You collaborate with the Destination Researcher and Accommodation Specialist 
    to optimize travel plans.""",
    verbose=True,
    memory=True,
    tools=[tools["maps"]],
    llm=llm,
    allow_delegation=True
)


