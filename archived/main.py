from langgraph.graph import StateGraph, END, START
from typing import TypedDict, List
from langchain_core.messages import SystemMessage
from openai import OpenAI
import os 
from scraper import fetch_repo_code
from hf_models import call_hf_summarization_agent

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="" + OPEN_AI_KEY,
)

def call_summarization_agent(message_content):
    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    extra_body={},
    model="x-ai/grok-code-fast-1",
    messages=[
        {
        "role": "user",
        "content": summary_extraction_prompt + " \n" + "```" + message_content + "```"
        }
    ]
    )
    return completion.choices[0].message.content


summary_extraction_prompt = """
Summarize the code for README generation.

Return JSON only:
{
  "file_name": "",
  "purpose": "",
  "key_components": [],
  "dependencies": [],
  "inputs_outputs": "",
  "important_logic": "",
  "connections": "",
  "configurations": "",
  "entry_point": ""
}

Guidelines:
- purpose: main role of the file
- key_components: main functions/classes (1-line each)
- dependencies: imports
- inputs_outputs: main I/O
- important_logic: key algorithms/flows
- connections: links to other modules/APIs
- configurations: constants/env vars
- entry_point: how execution starts if any

File:

"""


class AgentState(TypedDict):
    # repo_url: Annotated[str, add_messages] 
    repo_url : str
    file_summaries : List[SystemMessage]
    file_count : int
    i : int
    files : List[dict]
    

def initialization(state: AgentState):
    files = fetch_repo_code(state["repo_url"])
    return {
        "files": files,
        "file_count": len(files),
        "i": 0
    }

def summarize_the_current_file(state: AgentState):
    current_file = state["files"][state["i"]]
    file_name = current_file.get("path", "unknown_file")
    file_content = current_file.get("content", "")

    message_content = f"File name: {file_name}\n\n{file_content}"
    summarized_file = call_summarization_agent(message_content)
    print(summarized_file)

    updated_summaries = state.get("file_summaries", []) + [summarized_file]
    next_index = state["i"] + 1

    return {
        "file_summaries": updated_summaries,
        "i": next_index
    }



def should_continue(state: AgentState) -> AgentState:
    """Weather to continue the loop or not"""
    if state['i'] < state['file_count']:
        return "loop"
    else :
        return "exit"


def export_readme(state: AgentState):
    summaries_text = "\n\n".join(state.get("file_summaries", []))

    readme_generation_prompt = f"""
        You are a documentation generator. Use the provided file summaries to produce a clean, structured, and professional README.md.

        Requirements:
        - Output **only the README.md content**, with no explanations or meta-comments.
        - Do not include phrases like “based on the information provided” or “this README includes”.
        - Write in a concise, clear, and professional tone.

        The README must include:
        1. **Project Title & Overview**
        2. **Key Features**
        3. **Tech Stack**
        4. **Project Structure**
        5. **Setup Instructions**
        6. **Usage**
        7. **Contributing** (optional)
        8. **License** (optional)

        Insert code blocks where relevant.

        File summaries:
        {summaries_text}

        Generate the README now.

    """

    completion = client.chat.completions.create(
        model="x-ai/grok-code-fast-1",
        messages=[{"role": "user", "content": readme_generation_prompt}]
    )

    readme_content = completion.choices[0].message.content

    with open("DEMENTIA.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("\n✅ DEMENTIA.md file generated successfully as 'GENERATED_README.md'")
    return {"readme_content": readme_content}

def export_readme_hf(state: AgentState):
    """
    Generate a professional README.md using Hugging Face DeepSeek model
    based on the summarized file information in the state.
    """
    summaries_text = "\n\n".join(state.get("file_summaries", []))

    readme_generation_prompt = f"""
    You are an intelligent documentation generator.
    I will provide you with structured summaries of all files from a GitHub repository.

    Your task is to analyze all the provided information and generate a clean, well-formatted,
    and professional **README.md** for the repository.

    ### The README should include:
    1. **Project Title and Overview**
    2. **Key Features**
    3. **Tech Stack**
    4. **Project Structure**
    5. **Setup Instructions**
    6. **Usage**
    7. **Contributing (Optional)**
    8. **License (Optional)**

    Here are the summarized file details:
    {summaries_text}
    """
    client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
    )   

    # Use Hugging Face InferenceClient
    completion = client.chat.completions.create(
        model="x-ai/grok-code-fast-1",
        messages=[{"role": "user", "content": readme_generation_prompt}]
    )

    readme_content = completion.choices[0].message.content

    # Write to README.md
    with open("limuthu-repo.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("\n✅ limuthu-repo.md file generated successfully as 'GENERATED_README.md'")
    return {"readme_content": readme_content}



graph = StateGraph(AgentState)

graph.add_node("Initialization", initialization)
graph.add_edge(START, "Initialization")
graph.add_node("summarize", summarize_the_current_file)
graph.add_edge("Initialization", "summarize")
graph.add_conditional_edges(
    "summarize", 
    should_continue, 
    {
        "loop" : "summarize", 
        "exit" : "Export_README"
    }
)
graph.add_node("Export_README", export_readme)
graph.add_edge("Export_README", END)
app = graph.compile()


app.invoke({"repo_url" : "https://github.com/Team-XPredators/Dementia-Prediction-xpredators/"}, {"recursion_limit": 100})