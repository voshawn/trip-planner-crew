from crewai import Agent
from crewai_tools import SerperDevTool, WebsiteSearchTool
from dotenv import load_dotenv
from langchain_community.agent_toolkits.amadeus.toolkit import AmadeusToolkit
from langchain_community.chat_models import ChatOpenAI

from tools.calculator_tools import CalculatorTools

# Instantiate tools
load_dotenv()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

amadeus_toolkit = AmadeusToolkit()
amadeus_tools = amadeus_toolkit.get_tools()

# Load chat model
llm = ChatOpenAI(model="gpt-4-turbo")
# llm = ChatOpenAI(model="gpt-3.5-turbo")


class TripAgents:
    def city_selection_agent(self):
        return Agent(
            role="City Selection Expert",
            goal="Select the best city based on weather, season, and prices",
            backstory="An expert in analyzing travel data to pick ideal destinations",
            tools=[search_tool, web_rag_tool],
            llm=llm,
            verbose=True,
        )

    def local_expert(self):
        return Agent(
            role="Local Expert at this city",
            goal="Provide the BEST insights about the selected city",
            backstory="""A knowledgeable local guide with extensive information
        about the city, it's attractions and customs""",
            tools=[search_tool, web_rag_tool],
            llm=llm,
            verbose=True,
        )

    def travel_concierge(self):
        return Agent(
            role="Amazing Travel Concierge",
            goal="""Create the most amazing travel itineraries with budget and 
        packing suggestions for the city""",
            backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
            tools=[CalculatorTools.calculate] + amadeus_tools,
            llm=llm,
            verbose=True,
        )
