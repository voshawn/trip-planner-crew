import re
import sys
import time
from textwrap import dedent

import streamlit as st
from crewai import Crew
from dotenv import load_dotenv

from trip_agents import TripAgents
from trip_tasks import TripTasks

load_dotenv()


class TripCrew:
    def __init__(self, origin, destination, date_range, preferences):
        self.origin = origin
        self.destination = destination
        self.date_range = date_range
        self.preferences = preferences

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()

        local_tour_guide = agents.local_tour_guide()
        travel_cost_researcher = agents.travel_cost_researcher()
        travel_concierge_planner = agents.travel_concierge_planner()

        gather_task = tasks.gather_local_recommendations(
            local_tour_guide, self.destination, self.date_range, self.preferences
        )
        research_cost_task = tasks.research_travel_costs(
            travel_cost_researcher,
            self.origin,
            self.destination,
            self.date_range,
            self.preferences,
        )

        plan_task = tasks.plan_itinerary(
            travel_concierge_planner,
            self.origin,
            self.destination,
            self.date_range,
            self.preferences,
        )

        crew = Crew(
            agents=[local_tour_guide, travel_cost_researcher, travel_concierge_planner],
            tasks=[gather_task, research_cost_task, plan_task],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# display the console processing on streamlit UI
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ["red", "green", "blue", "orange"]  # Define a list of colors
        self.color_index = 0  # Initialize color index

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r"\x1B\[[0-9;]*[mK]", "", data)
        # Remove section dividers
        cleaned_data = cleaned_data.replace("---", "")

        # Check if the data contains 'task' information
        task_match_object = re.search(
            r"\"task\"\s*:\s*\"(.*?)\"", cleaned_data, re.IGNORECASE
        )
        task_match_input = re.search(
            r"task\s*:\s*([^\n]*)", cleaned_data, re.IGNORECASE
        )
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            # Apply different color and switch color index
            self.color_index = (self.color_index + 1) % len(
                self.colors
            )  # Increment color index and wrap around if necessary

            cleaned_data = cleaned_data.replace(
                "Entering new CrewAgentExecutor chain",
                f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]",
            )

        if "Local Expert at this Destination" in cleaned_data:
            # Apply different color
            cleaned_data = cleaned_data.replace(
                "Local Expert at this Destination",
                f":{self.colors[self.color_index]}[Local Expert at this Destination]",
            )
        if "Travel Cost Researcher" in cleaned_data:
            cleaned_data = cleaned_data.replace(
                "Travel Cost Researcher",
                f":{self.colors[self.color_index]}[Travel Cost Researcher]",
            )
        if "Personal Travel Concierge" in cleaned_data:
            cleaned_data = cleaned_data.replace(
                "Personal Travel Concierge",
                f":{self.colors[self.color_index]}[Personal Travel Concierge]",
            )
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace(
                "Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]"
            )

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown("".join(self.buffer), unsafe_allow_html=True)
            self.buffer = []


# Streamlit interface
def run_crewai_app():
    st.title("Your AI Trip Planning Crew")
    with st.expander("About the Team:"):
        st.header("Overview")
        st.text("""       
        This crew has 3 experts that work together to design your perfect trip. 
        Each agent has a specific role and task to complete.
        They are able to use tools that have been provided to them. 
        These Agents are run via OpenAPI GPT-4 model.""")

        st.subheader("1) Local Expert at this Destination")
        st.text("""       
        Goal = Provide the BEST insights about the destination
        Tools = Able to search the web and summarize key information""")

        st.subheader("2) Travel Cost Researcher")
        st.text("""       
        Goal = Provide accurate and precise hotel, flight, and 
               transporation recommendations and costs for the trip
        Tools = Able to look up flight data, search the web, and calcuate costs.""")

        st.subheader("3) Personal Travel Concierge")
        st.text("""       
        Goal = Curate the most amazing and personalized travel itineraries 
               with budget, safety information, local customs information, 
               packing suggestions, and travel tips for the city
        Tools = Can do basic arithmetic.""")

    origin = st.text_input("From where will you be traveling from?")
    destination = st.text_input("Where will you be traveling to?")
    date_range = st.text_input(
        "What is the date range you are interested in traveling?"
    )
    preferences = st.text_input("What are some of your travel perferences?")

    if st.button("Run Analysis"):
        # Placeholder for stopwatch
        stopwatch_placeholder = st.empty()

        # Start the stopwatch
        start_time = time.time()
        with st.expander("Processing... See our work:"):
            sys.stdout = StreamToExpander(st)
            with st.spinner("Generating Results"):
                trip_crew = TripCrew(origin, destination, date_range, preferences)
                crew_result = trip_crew.run()

        # Stop the stopwatch
        end_time = time.time()
        total_time = end_time - start_time
        stopwatch_placeholder.text(f"Total Time Elapsed: {total_time:.2f} seconds")

        st.header("Final Results Below:")
        st.divider()
        st.markdown(crew_result)


if __name__ == "__main__":
    run_crewai_app()

## Uncomment this code to run the app in the terminal

# if __name__ == "__main__":
#     print("## Welcome to Trip Planner Crew")
#     print("-------------------------------")
#     origin = input(
#         dedent("""
#       From where will you be traveling from?
#     """)
#     )
#     destination = input(
#         dedent("""
#       Where are you interested in visiting?
#     """)
#     )
#     date_range = input(
#         dedent("""
#       What is the date range you are interested in traveling?
#     """)
#     )
#     preferences = input(
#         dedent("""
#       What are some of your travel perferences? Include things like
#     hobbies, interests, or any special requests.
#     """)
#     )

#     trip_crew = TripCrew(origin, destination, date_range, preferences)
#     result = trip_crew.run()
#     print("\n\n########################")
#     print("## Here is you Trip Plan")
#     print("########################\n")
#     print(result)
