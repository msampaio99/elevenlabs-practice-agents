# ElevenLabs practice agents

I made this while trying out ElevenLabs Agents for two things I actually wanted to practice:

- speaking Italian more naturally (so I can talk to my inlaws!)
- talking through my past engineering work as interview prep


This repo has two small pieces of work that I wanted to add beyond the functionality straight out the box:

1. a Python runner for starting an ElevenLabs conversation locally
2. a tiny read-only API that the interview agent can call as a webhook tool to retrieve structured context about a project (especifically my past engineering projects)

I intentionally kept this small. The goals was to better understand how building with ElevenLabs works and build something that would help me in my personal life.

---

## The Agents

### Italian Language Practice Tutor

I wanted this agent to practice mostly conversation and get me talking! But always gently correcting my grammer and improving upon my articulation.

For me it was important for the agent to:

- keep me talking
- correct important mistakes without it becoming a grammar lesson (how a normal speaker would gently correct me)
- adjust the difficulty if I was struggling
- make it feel like a natural conversation (it it did and i walked away impressed honestly)


### Technical Interview Coach

While preparing for tech interviews I wanted to practice talking about past projects in concise and structured ways that also hit all the "points."

I wanted my interview coach to ask me things like:

- what I personally owned
- architecture and implementation choices
- tradeoffs
- failure modes
- how I knew something worked or succeeded
- what could be standardized or automated
- how I would explain the same project to different audiences (marketing, engineering, product, sales, customer, etc.)

I wanted the Agent to be able to retrieve relevant context about my projects (kind of like how an interviewer would glance at my resume while interviewing me.) Instead of uploading my resume to the prompt, I wanted to use this as an opportunity to learn how building upon an ElevenLabs agent looks like so instead I created a small webhook integration.


# Webhook integration

The Technical Interview Coach agent can call a small REST API to retrieve structured context about one of my past projects.

The flow is:

```text
voice conversation
      |
      v
ElevenLabs Agent
      |
      | decides it needs project context
      v
get_project_context webhook tool
      |
      | GET /projects/{project_id}
      v
small FastAPI service
      |
      v
projects.json
      |
      v
structured project context returned to the agent
      |
      v
agent asks a grounded follow-up question
```


For just 3 project summaries, a JSON file was the way to go instead of a full database or vector store.

The part I wanted to explore was the **integration boundary**:

- how the agent knows when to call a tool
- how the tool parameter is described
- how everything gets configured within the ElevenLabs dashboard
- how the agent actually used the response in conversation!

---

# Files in this repo

```text
.
├── README.md
├── run_agent.py
├── project_api.py
├── projects.json
├── requirements.txt
└── prompts/
    ├── italian.txt
    └── interview.txt
```

---

# How to actually run this thing

# Part 1: Run an ElevenLabs agent locally - Built for the Italian Language Coach Agent

This uses the ElevenLabs Python SDK.

## 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```


## 2. Install dependencies

```bash
pip install -r requirements.txt
```


## 3. Add your agent ID

Edit `.env`:

```text
AGENT_ID=your_agent_id_here
ELEVENLABS_API_KEY=
```

## 4. Start the conversation

```bash
python run_agent.py
```

---

# Part 2: Run the project-context API - Built for the Technical Interview Coach Agent

The API is implemented with FastAPI (read-only and intentionally lightweight)

## 1. Start API

From repo root:

```bash
uvicorn project_api:app --reload --port 8000
```

server will be on:

```text
http://127.0.0.1:8000
```

## 2. Check health

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## 3. List available projects

```bash
curl http://127.0.0.1:8000/projects
```

The current IDs are:

```text
koneksa-gitops
rapid7-eks-migration
legit-fish-client-integration
```

## 4. Fetch one project

```bash
curl http://127.0.0.1:8000/projects/koneksa-gitops
```

The response includes:

- summary
- problem
- my contribution
- technologies
- interview angles
- guardrails

The `guardrails` field reminds the agent not to invent things like metrics, customer names, or implementation details that are not present.

---

# Part 3: Make the local API reachable by ElevenLabs


To expose the local FastAPI service through an HTTPS tunnel I used ngrok

You want to install ngrok, and then keep the FastAPI server running and open another terminal:

```bash
ngrok http 8000
```

ngrok will print a public HTTPS URL, for example:

```text
https://example.ngrok-free.app
```

Your tool endpoint would then be:

```text
https://example.ngrok-free.app/projects/{project_id}
```

---

# Part 4: Configure the ElevenLabs webhook tool

This part all takes place in the ElevenLabs dashboard

# Part 5: Test integrationg by prompting the agent with a topic it would need more context on

Here is an example of how I prompted mine and how it successfully responded with added context:
<img width="1593" height="834" alt="Screenshot 2026-10-08 at 2 54 02 PM" src="https://github.com/user-attachments/assets/ddbb3115-a683-49d7-ab2b-6dca6106f540" />



If successfull you will see on the dashboard that the webhook successfully ran:
<img width="1592" height="826" alt="Screenshot 2026-10-08 at 1 46 46 PM" src="https://github.com/user-attachments/assets/071d841b-f0c7-494f-9629-d0d0ec6d7fe7" />



---

# Important security and privacy note 

For a production API, I would not leave the endpoint publicly readable like this. I would add authentication and appropriate authorization.

The unauthenticated read-only endpoint is a deliberate simplification for a personal demo using non-sensitive project summaries.

---

# Next things I would try

I would like play around with adding:

- authentication to the API
- a small database rather than a JSON file
- a tool that performs an action rather than only fetching data
