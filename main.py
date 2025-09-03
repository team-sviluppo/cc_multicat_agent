from cat.mad_hatter.decorators import hook, tool, plugin
from cat.looking_glass.cheshire_cat import CheshireCat
from langchain.docstore.document import Document
from cat.log import log
from cat.env import get_env
import requests, json

ccat = CheshireCat()


@plugin
def save_settings(settings):
    orchestrator_url = settings["orchestrator_url"]
    orchestrator_key = settings["orchestrator_key"]
    agent_name = settings["agent_name"]
    agent_description = settings["agent_description"]
    agent_url = get_env("CCAT_CORE_HOST")
    agent_port = get_env("CCAT_CORE_PORT")
    agent_key = get_env("CCAT_API_KEY_WS")
    agent_ssl = get_env("CCAT_CORE_USE_SECURE_PROTOCOLS")
    if agent_url == "localhost":
        # if in same docker compose stack with localhost convert it to docker hostname
        agent_url = "host.docker.internal"
    register_agent(
        orchestrator_url,
        orchestrator_key,
        agent_name,
        agent_description,
        agent_url,
        agent_port,
        agent_key,
        agent_ssl,
    )


def register_agent(
    orchestrator_url,
    orchestrator_key,
    agent_name,
    agent_description,
    agent_url,
    agent_port,
    agent_key,
    agent_ssl,
):
    try:
        url = orchestrator_url.rstrip("/") + "/multicat/register-agent"
        # register agent on orchestrator
        log.info(f"Registering agent '{agent_name}' on orchestrator at {url}")
        # Here you would add the code to register the agent with the orchestrator
        payload = {
            "agent_name": agent_name,
            "agent_description": agent_description,
            "agent_url": agent_url,
            "agent_port": agent_port,
            "agent_key": agent_key,
            "agent_ssl": agent_ssl,
        }
        headers = {
            "Authorization": f"Bearer {orchestrator_key}",
            "Content-Type": "application/json",
        }
        log.info(f"Registering agent to {url} with payload: {json.dumps(payload)}")
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        log.info(f"Agent registered successfully: {resp.status_code} {resp.text}")
    except Exception as e:
        log.error(f"Failed to register agent: {e}")


@plugin
def activated(plugin):
    settings = ccat.mad_hatter.get_plugin().load_settings()
    orchestrator_url = settings["orchestrator_url"]
    orchestrator_key = settings["orchestrator_key"]
    agent_name = settings["agent_name"]
    agent_description = settings["agent_description"]
    agent_url = get_env("CCAT_CORE_HOST")
    agent_port = get_env("CCAT_CORE_PORT")
    agent_key = get_env("CCAT_API_KEY_WS")
    agent_ssl = get_env("CCAT_CORE_USE_SECURE_PROTOCOLS")
    if agent_url == "localhost":
        # if in same docker compose stack with localhost convert it to docker hostname
        agent_url = "host.docker.internal"
    register_agent(
        orchestrator_url,
        orchestrator_key,
        agent_name,
        agent_description,
        agent_url,
        agent_port,
        agent_key,
        agent_ssl,
    )


@plugin
def deactivated(plugin):
    settings = ccat.mad_hatter.get_plugin().load_settings()
    agent_name = settings["agent_name"]
    log.info(f"Deactivating agent: {agent_name}")
    orchestrator_url = settings["orchestrator_url"]
    orchestrator_key = settings["orchestrator_key"]
    try:
        url = orchestrator_url.rstrip("/") + f"/multicat/delete-agent/{agent_name}"
        headers = {
            "Authorization": f"Bearer {orchestrator_key}",
        }
        log.info(f"Deleting agent at {url}")
        resp = requests.delete(url, headers=headers, timeout=10)
        resp.raise_for_status()
        log.info(f"Agent deleted successfully: {resp.status_code} {resp.text}")
    except Exception as e:
        log.error(f"Failed to delete agent: {e}")


@hook(priority=99)
def before_rabbithole_insert_memory(doc: Document, cat) -> Document:
    settings = ccat.mad_hatter.get_plugin().load_settings()
    agent_name = settings["agent_name"]
    doc.metadata["agent"] = agent_name
    return doc


@hook(priority=99)
def before_cat_recalls_declarative_memories(
    declarative_recall_config: dict, cat
) -> dict:
    settings = ccat.mad_hatter.get_plugin().load_settings()
    agent_name = settings["agent_name"]
    declarative_recall_config["metadata"] = {"agent": agent_name}

    return declarative_recall_config
