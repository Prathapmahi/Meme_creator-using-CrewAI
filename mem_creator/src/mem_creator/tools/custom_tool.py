from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import requests

class MemeTemplateInput(BaseModel):
    """Input schema for MemeTemplateTool."""
    query: str = Field(..., description="Meme template name or keyword to search for.")

class MemeTemplateTool(BaseTool):
    name: str = "Meme Template Fetcher"
    description: str = "Fetches meme templates from Imgflip API based on a query."
    args_schema: Type[BaseModel] = MemeTemplateInput

    def _run(self, query: str) -> dict:
        url = "https://api.imgflip.com/get_memes"
        response = requests.get(url)
        if response.status_code == 200:
            memes = response.json().get("data", {}).get("memes", [])
            for meme in memes:
                if query.lower() in meme["name"].lower():
                    return {"name": meme["name"], "url": meme["url"]}
        return {"error": "No meme template found"}
