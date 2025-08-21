## crew.py
from crewai import Crew
from agent import meme_ideator, image_selector, caption_writer
from task import ideation_task, image_selection_task, caption_task

crew = Crew(
    agents=[meme_ideator, image_selector, caption_writer],
    tasks=[ideation_task, image_selection_task, caption_task],
    model="gemini/gemini-1.5-pro",
    api_key="GEMINI_API_KEY"
)

def run_crew(user_input):
    return crew.execute(user_input)