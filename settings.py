from pydantic import BaseModel
from cat.mad_hatter.decorators import plugin
from enum import Enum


# Plugin settings
class PluginSettings(BaseModel):
    orchestrator_url: str = ""
    orchestrator_key: str = ""
    agent_name: str = ""
    agent_description: str = ""


# hook to give the cat settings
@plugin
def settings_schema():
    return PluginSettings.schema()
