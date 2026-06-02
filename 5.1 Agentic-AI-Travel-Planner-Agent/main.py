import os
import sys
import certifi
import requests
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool
from langchain.agents import create_react_agent, AgentExecutor

# ==========================================
# LOAD ENV VARIABLES
# ==========================================
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

OPENAI_API_KEY        = os.getenv("OPENAI_API_KEY")
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
TAVILY_API_KEY        = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY  = os.getenv("WEATHERSTACK_API_KEY")

# ==========================================
# TOOLS
# ==========================================

search_tool = TavilySearchResults(max_results=4)


@tool
def get_exchange_rate(currency_pair: str) -> str:
    """
    Get exchange rate between two currencies.
    Example: INR,JPY  or  USD,INR  or  EUR,JPY
    """
    from_currency, to_currency = [c.strip().upper() for c in currency_pair.split(",")]
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    rate = data["conversion_rates"][to_currency]
    return f"1 {from_currency} = {rate} {to_currency}"


@tool
def get_weather_data(city: str) -> str:
    """Fetch current weather information for a city."""
    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )
    response = requests.get(url)
    data = response.json()
    if "current" not in data:
        return f"Could not fetch weather data for {city}"
    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%\n"
        f"Wind Speed: {data['current']['wind_speed']} km/h\n"
        f"Feels Like: {data['current']['feelslike']}°C"
    )


@tool
def get_country_info(country: str) -> str:
    """
    Fetch country information including capital, currency,
    population, region, languages, flag and country codes.
    """
    url = (
        f"https://restcountries.com/v3.1/name/{country}"
        "?fields=name,capital,currencies,population,region,languages,flags,cca2,cca3"
    )
    response = requests.get(url)
    data = response.json()
    if not data or isinstance(data, dict):
        return f"Could not fetch country information for {country}"
    country_data = data[0]
    currency_code = list(country_data["currencies"].keys())[0]
    currency_name = country_data["currencies"][currency_code]["name"]
    languages = ", ".join(country_data["languages"].values())
    return (
        f"Country: {country_data['name']['common']}\n"
        f"Capital: {country_data['capital'][0]}\n"
        f"Region: {country_data['region']}\n"
        f"Population: {country_data['population']:,}\n"
        f"Currency: {currency_name} ({currency_code})\n"
        f"Languages: {languages}\n"
        f"Country Code: {country_data['cca2']} / {country_data['cca3']}\n"
        f"Flag: {country_data['flags']['png']}"
    )


tools = [search_tool, get_weather_data, get_exchange_rate, get_country_info]

# ==========================================
# LLM
# ==========================================
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    temperature=0,
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    max_tokens=500
)

# ==========================================
# PROMPT
# ==========================================
prompt = hub.pull("hwchase17/react")

# ==========================================
# CREATE AGENT
# ==========================================
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# ==========================================
# EXECUTOR
# ==========================================
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# ==========================================
# CLI LOOP
# ==========================================
BANNER = """
╔══════════════════════════════════════════════════════╗
║          ✈   AI Travel Agent  (CLI Mode)   ✈        ║
║  Tools: Country Info · Weather · Exchange · Search   ║
║  Type  'exit' or 'quit' to stop                      ║
╚══════════════════════════════════════════════════════╝
"""

def main():
    print(BANNER)

    while True:
        try:
            user_query = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye! ✈")
            sys.exit(0)

        if not user_query:
            continue

        if user_query.lower() in {"exit", "quit"}:
            print("Goodbye! ✈")
            sys.exit(0)

        print()  # blank line before agent trace

        try:
            response = agent_executor.invoke({"input": user_query})
            print("\n" + "─" * 54)
            print("FINAL ANSWER")
            print("─" * 54)
            print(response["output"])
            print("─" * 54 + "\n")

        except Exception as e:
            print(f"\n[ERROR] {e}\n")


if __name__ == "__main__":
    main()