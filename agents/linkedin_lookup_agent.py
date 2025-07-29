from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub as prompt

from tools.tools import get_profile_url_tavily


# take a name and return the url of linkedin profile
def lookup(name: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    template = """
    given the full name {name_of_person}, I want you to give me the link to their Linkedin profile page.
    you should only return the URL value without format and transformation
    """

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )

    tools_for_agent = [
        Tool(
            name="Search for Linkedin profile page",
            func=get_profile_url_tavily,
            # tell llm what is this tool for and llm will decide when to use it
            description="use this when need to get a Linkedin Page URL",
        )
    ]

    react_prompt = prompt.pull("anandbhaskaran/react-system-prompt")

    agent = create_react_agent(llm=llm, prompt=react_prompt, tools=tools_for_agent)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    input = prompt_template.format_prompt(name_of_person=name)

    result = agent_executor.invoke(input={"input": input})

    return result.get("output")


if __name__ == "__main__":
    url = lookup("alexkaizhang")
    print(url)
