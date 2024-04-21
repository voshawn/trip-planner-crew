from crewai import Agent
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool
)
from langchain.llms import OpenAI
from tools.calculator_tools import CalculatorTools
from dotenv import load_dotenv

# Instantiate tools
load_dotenv()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()


class TripAgents():

  def city_selection_agent(self):
    return Agent(
        role='City Selection Expert',
        goal='Select the best city based on weather, season, and prices',
        backstory=
        'An expert in analyzing travel data to pick ideal destinations',
        tools=[search_tool, web_rag_tool],
        verbose=True)

  def local_expert(self):
    return Agent(
        role='Local Expert at this city',
        goal='Provide the BEST insights about the selected city',
        backstory="""A knowledgeable local guide with extensive information
        about the city, it's attractions and customs""",
        tools=[
           search_tool, web_rag_tool 
        ],
        verbose=True)

  def travel_concierge(self):
    return Agent(
        role='Amazing Travel Concierge',
        goal="""Create the most amazing travel itineraries with budget and 
        packing suggestions for the city""",
        backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
        tools=[
            CalculatorTools.calculate,
        ],
        verbose=True)