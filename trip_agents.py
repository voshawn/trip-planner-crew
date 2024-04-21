from textwrap import dedent

from crewai import Agent
from crewai_tools import SerperDevTool, WebsiteSearchTool
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools.amadeus.closest_airport import AmadeusClosestAirport
from langchain_community.tools.amadeus.flight_search import AmadeusFlightSearch

from tools.calculator_tools import CalculatorTools

# Instantiate tools
load_dotenv()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()
closest_airport_tool = AmadeusClosestAirport()
flight_search_tool = AmadeusFlightSearch()


# Load chat model
llm = ChatOpenAI(model="gpt-4-turbo")
# llm = ChatOpenAI(model="gpt-3.5-turbo")


class TripAgents:
    def local_tour_guide(self):
        return Agent(
            role="Local Expert at this Destination",
            goal=dedent("""Provide the BEST insights about the destination"""),
            backstory=dedent("""A knowledgeable local guide with extensive information
        about the destination, it's weather forecasts, attractions, accomodations, 
        local transportation options, and customs. Has been a local tour guide
        at this city for decades."""),
            tools=[search_tool, web_rag_tool],
            llm=llm,
            verbose=True,
            allow_delegation=False,
        )

    def travel_cost_researcher(self):
        return Agent(
            role="Travel Cost Researcher",
            goal=dedent("""Provide accurate and precise hotel, flight, and 
            transporation recommendations and costs for the trip"""),
            backstory=dedent("""A precise researcher that is able to find hotel, 
        flights, and transportation costs traveling to and within a location."""),
            tools=[
                closest_airport_tool,
                flight_search_tool,
                search_tool,
                web_rag_tool,
                CalculatorTools.calculate,
            ],
            llm=llm,
            verbose=True,
            allow_delegation=False,
        )

    def travel_concierge_planner(self):
        return Agent(
            role="Personal Travel Concierge",
            goal=dedent("""Curate the most amazing and personalized travel itineraries 
            with budget, safety information, local customs information, 
            packing suggestions, and travel tips for the city"""),
            backstory="""Specialist in travel planning and logistics with 
        decades of experience. Has planned trips for thousands of highly particular 
        clients""",
            tools=[CalculatorTools.calculate],
            llm=llm,
            verbose=True,
            allow_delegation=False,
        )
