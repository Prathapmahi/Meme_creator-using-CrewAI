from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool  # Import @tool decorator
from dotenv import load_dotenv
import os

load_dotenv()

@tool("Meme Template Fetcher")
def fetch_meme_template(query: str) -> str:
    """Fetches a meme template based on a keyword."""
    meme_templates = {
        "distracted boyfriend": "https://i.imgflip.com/1ur9b0.jpg",
        "drake hotline bling": "https://i.imgflip.com/30b1gx.jpg",
        "two buttons": "https://i.imgflip.com/1g8my4.jpg"
    }
    return meme_templates.get(query.lower(), "No matching meme template found.")

# Initialize LLM model
geminillm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.environ["GEMINI_API_KEY"],
)

@CrewBase
class MemCreator:
    """MemeCreator crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Ensure that agents are initialized correctly
        self.researcher_agent = self.researcher()
        self.image_selector_agent = self.image_selector_agent()
        self.caption_writer_agent = self.caption_writer_agent()

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['meme_ideator'],  # Ensure this matches the YAML
            verbose=True,
            tools=[fetch_meme_template],
            llm=geminillm
        )

    @agent
    def image_selector_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['image_selector'],  # Ensure this matches the YAML
            verbose=True,
            tools=[fetch_meme_template],
            llm=geminillm
        )

    @agent
    def caption_writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['caption_writer'],  # Ensure this matches the YAML
            verbose=True,
            tools=[fetch_meme_template],
            llm=geminillm
        )

    @task
    def ideation_task(self) -> Task:
        return Task(
            config=self.tasks_config['ideation_task'],
            output_file='report.md'
        )

    @task
    def image_selection_task(self) -> Task:
        return Task(
            config=self.tasks_config['image_selection_task'],
            output_file='report.md'
        )

    @task
    def caption_task(self) -> Task:
        return Task(
            config=self.tasks_config['caption_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MemCreator crew"""
        return Crew(
            agents=[self.researcher_agent, self.image_selector_agent, self.caption_writer_agent],
            tasks=[self.ideation_task(), self.image_selection_task(), self.caption_task()],
            process=Process.sequential,
            verbose=True,
        )