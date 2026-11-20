from agent import build_agent, build_remembered_agent


def main():
    Thread_ID = input("\nEnter thread ID. The default is 'default': ").strip()
    Show_tool_calls = input("Show tool calls? (y/n): ").strip().lower()
    Remember_agent = input("Do you want the agent to remember you next time? (y/n): ").strip().lower()
    
    if not Thread_ID:
        config = {"configurable": {"thread_id": "default"}}
    else:
        config = {"configurable": {"thread_id": Thread_ID}}

    if Show_tool_calls == "y" or Show_tool_calls == "yes":
        stream_mode = ["messages", "updates"]
    elif Show_tool_calls == "n" or Show_tool_calls == "no" or Show_tool_calls == "":
        stream_mode = "messages"
    
    
        
        
    try:    
        if Remember_agent == "y" or Remember_agent == "yes":
            agent = build_remembered_agent()
        elif Remember_agent == "n" or Remember_agent == "no" or Remember_agent == "":
            agent = build_agent()
    except Exception as error:
        print(f"Error while building the agent: {error}")
        return
    
    
    
    while True:
        user_input = input("\nEnter your message. Or write 'exit' or 'quit' to stop. ")
        if user_input.strip().lower() in ["exit", "quit"]:
            break
        elif not user_input.strip():
            continue
        
        messages = {"messages": [{"role": "user", "content": user_input}]}
        
        try:
            for chunk in agent.stream(messages,config=config, stream_mode=stream_mode, version="v2"):
                if chunk["type"] == "messages":
                    token, metadata = chunk["data"]
                    if token.content and metadata.get("langgraph_node") == 'model':
                        print(token.content, end="", flush=True)
                        
                elif chunk["type"] == "updates":
                    for node, state_update in chunk["data"].items():
                        if node == "tools":
                            print(f"{"-"*10}\nTool called: {state_update["messages"][0].name} \nTool result: {state_update["messages"][0].content}\n {"-"*10}", flush=True)
                    
        except Exception as error: 
            print(f"Error while streaming the agent's response: {error}")
            break
    
    
    
    

if __name__ == "__main__":
    main()