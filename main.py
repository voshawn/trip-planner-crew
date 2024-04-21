from textwrap import dedent

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


if __name__ == "__main__":
    print("## Welcome to Trip Planner Crew")
    print("-------------------------------")
    origin = input(
        dedent("""
      From where will you be traveling from?
    """)
    )
    destination = input(
        dedent("""
      Where are you interested in visiting?
    """)
    )
    date_range = input(
        dedent("""
      What is the date range you are interested in traveling?
    """)
    )
    preferences = input(
        dedent("""
      What are some of your travel perferences? Include things like 
    hobbies, interests, or any special requests.
    """)
    )

    trip_crew = TripCrew(origin, destination, date_range, preferences)
    result = trip_crew.run()
    print("\n\n########################")
    print("## Here is you Trip Plan")
    print("########################\n")
    print(result)
