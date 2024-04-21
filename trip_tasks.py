from textwrap import dedent

from crewai import Task


class TripTasks:
    def gather_local_recommendations(self, agent, destination, date_range, preferences):
        return Task(
            description=dedent(f"""
        As a local expert on this destination you must compile an 
        in-depth guide for someone traveling there and wanting 
        to have the best trip according to their travel preferences. 
        Gather information about  key attractions, local customs,
        Find the best spots to go to, the kind of place only a
        local would know.
        special events, and daily activity recommendations.
        Provide custom recommendations for hotels, restaurants, 
        and transportation options to and from these locations. 
        This guide should provide a thorough overview of what 
        the city has to offer, including hidden gems, cultural
        hotspots, must-visit landmarks, weather forecasts, and
        high level costs.
        
        Destination: {destination}
        Trip Date Range: {date_range}
        Traveler Preferences: {preferences}
      """),
            expected_output=dedent("""
        The final answer must be a comprehensive city guide, 
        rich in cultural insights and practical tips, with accommodation 
        and transporation options. These recommendations should be tailored to 
        the traveler preferences.
        """),
            agent=agent,
        )

    def research_travel_costs(
        self, agent, origin, destination, date_range, preferences
    ):
        return Task(
            description=dedent(f"""
        Expand this guide to include expected travel costs. 
        
        You must research actual cost information and provide 
        options that are inexpensive, concvenient, and comfortable.

        Please consider the availability of Uber as well as AirBnB
        in addition to traditional Taxis and Hotels.  
        
        These costs shoud cover all aspects of the trip, 
        from arrival to departure. 

        When searching for flights, you must provide the following four parameters 
        EXACTLY as shown below:
        "originLocationCode" 
        "destinationLocationCode"
        "departureDateTimeEarliest"
        "departureDateTimeLatest"
        Please double check the spelling and format of these parameters.
                               
        Earliest and Latest departure dates need to be the same date and
        and in the format of '%Y-%m-%dT%H:%M:%S'. 
        
        If you're trying to search for round-trip  flights, call this function for the 
        outbound flight first, and then call again for the return flight. 
        
        Use the Currency of USD for all Costs and Prices.

        Origin: {origin}
        Destination: {destination}
        Trip Date Range: {date_range}
        Traveler Preferences: {preferences}
        """),
            expected_output=dedent("""
        Your final answer MUST be a well-researched analysis of all the travel costs
        associated with the trip, including flights, hotels, and local transportation.
        Provide flight specific details between the origin and destination.  
        """),
            agent=agent,
        )

    def plan_itinerary(self, agent, origin, destination, date_range, preferences):
        return Task(
            description=dedent(f"""
        Expand this guide into a full travel  itinerary with detailed per-day plans, 
        including weather forecasts, places to eat, packing suggestions, 
        transportation recommendations, accomodation recommendationsm, 
        and a budget breakdown.
        
        You MUST suggest actual places to visit, actual hotels 
        to stay, actual transportation options, and actual restaurants to go to.

        You MUST suggest the actual arrival and departure dates and times based on 
        the most affordable options.
                                 
        This itinerary should cover all aspects of the trip, 
        from arrival to departure, integrating the city guide
        information with practical travel logistics.
        
        Origin: {origin}
        Desination: {destination}
        Trip Date Range: {date_range}
        Traveler Preference: {preferences}
        """),
            expected_output=dedent("""
        Your final answer MUST be a complete expanded travel plan,
        formatted as markdown, encompassing a daily schedule,
        anticipated weather conditions, recommended clothing and
        items to pack, flight suggestions, accomodation options, 
        and a detailed budget, ensuring THE BEST TRIP EVER.
        Be specific and give it a reason why you picked each option, 
        ans how it matches the traveler preferences! 
        """),
            agent=agent,
        )
