# main file is main.py


# function to invoke the agent using query and config
def call_agent(user_query, config, agent):
    return agent.invoke({'input': user_query}, config=config)

