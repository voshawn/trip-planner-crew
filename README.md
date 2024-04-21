# Trip Planner Crew

This is a multi agent system to plan your trips.

It features 3 agents that will

1. Provide local tour guide tips using Google Search
2. Research costs of the travel using Google Search and Amadeus APIs
3. Construct a personalized day-by-day itinerary.

### Getting Started

1. Ensure you have `python3` and `poetry` installed.
2. Set your `.env` with the following keys

```
SERPER_API_KEY= #Used for searching google
OPENAI_API_KEY= #Used for the LLM
AMADEUS_CLIENT_ID= #Used for researching flights
AMADEUS_CLIENT_SECRET=
AMADEUS_HOSTNAME=
```

3. Run `poetry install`
4. Run `python3 main.py`

## Notes

1. This will use GPT-4 by default for best results, but may be a bit expensive.
