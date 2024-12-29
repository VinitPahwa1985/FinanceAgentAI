import logging  # Import the logging module
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.playground import Playground, serve_playground_app
import phi.api
import openai
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()
logging.info("Loaded environment variables from .env file")

# Access the variables
openai_api_key = os.getenv('OPENAI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
phi.api.api_key = os.getenv("PHI_API_KEY")

# Log the API keys to verify they are loaded correctly
logging.info(f"OpenAI API Key: {openai_api_key}")
logging.info(f"GROQ API Key: {GROQ_API_KEY}")
logging.info(f"PHI API Key: {phi.api.api_key}")

# Define the web search agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tools_calls=True,
    markdown=True,
)
logging.info("Web Search Agent created")

# Define the finance info agent
finance_agent = Agent(
    name="Finance Info Agent",
    role="Search the web for the information",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=["Use table to display data"],
    show_tools_calls=True,
    markdown=True,
)
logging.info("Finance Info Agent created")

# Create a Playground app with the defined agents
app = Playground(agents=[finance_agent, web_search_agent]).get_app()
logging.info("Playground app created with the defined agents")

# Serve the Playground app
if __name__ == "__main__":
    logging.info("Starting the Playground app")
    serve_playground_app("playground:app", reload=True)