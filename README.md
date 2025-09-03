# ⚡ Multicat Agent

**Multicat Agent** is a plugin part of Multicat, a multiagent system for Cheshire Cat AI. Multicat is composed by 2 plugins:

- **Orchestrator** (https://github.com/team-sviluppo/cc_multicat_orchestrator)
- **Agent**: (this plugin)

## 🚀 Quick Start

### Prerequisites

This plugin requires multiple Cheshire Cat instances with the **Multicat Orchestrator** plugin installed and configured

### Plugin Configuration

The plugin offers several configurable parameters:

- **Orchestrator Url**: The Orchestartor Url (with http:// or https://)
- **Orchestrator Key**: The API Key (for REST Endpoints) set to the Orchestrator instance
- **Agent name**: The name that identify this Agent
- **Agent description**: The description of this agent. The Orchestartor choose agentes using this description, so it need very accurate (example: "This agent is specialized to solve math problems or reply about math questions")

### Tech Info and Exmples

On Orchestrator repository https://github.com/team-sviluppo/cc_multicat_orchestrator is available one example of working Multicat System
