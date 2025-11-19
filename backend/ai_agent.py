from langchain_core.tools import tool
from tools import query_medgemma, call_emergency

@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone.
    """
    return query_medgemma(query)

@tool
def emergency_call_tool() -> None:
    """
    Place an emergency call to the safety helpline's phone number via Twilio.
    Use this only if the user expresses suicidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help.
    """
    call_emergency()

@tool
def locate_therapist_tool(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return (
        f"Here are some therapists near {location}, {location}:\n"
        "- Dr. Joshua bennett - +1 (452) 123-7845\n"
        "- Dr. James Monroe - +1 (125) 785-5874\n"
        "- MindHealth Counseling Center - +1 (703) 452-4528"
    )

# Create AI Agent and link to backend tools
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from config import OPENAI_API_KEY
from langchain_core.messages import AIMessage

tools = [ask_mental_health_specialist, emergency_call_tool, locate_therapist_tool]
llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.5, api_key=OPENAI_API_KEY)

graph = create_agent(model=llm, tools=tools)

SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `locate_therapist_tool`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.

Always take necessary action. Respond kindly, clearly, and supportively.
"""
def parse_response(stream):
    tool_called_name = "None"
    final_response = None

    for s in stream:
        model_messages = s.get("model", {}).get("messages", [])
        # Check if a tool was called
        tool_data = s.get('tools')
        if tool_data:
            tool_messages = tool_data.get('messages')
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    tool_called_name = getattr(msg, 'name', 'None')

        # Check if agent returned a message
        for msg in reversed(model_messages):
            if isinstance(msg, AIMessage):
                final_response = msg.content  # this is your final AI answer

    return tool_called_name, final_response

""" if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        print(f"Received user input: {user_input[:200]}...")
        inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]}
        stream = graph.stream(inputs, stream_mode="updates")
        tool_called_name, final_response = parse_response(stream)
        print("TOOL CALLED: ", tool_called_name)
        print("ANSWER: ", final_response) """


