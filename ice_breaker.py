from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile

from agents.linkedin_lookup_agent import lookup


def ice_break_with(name: str):

    # step 1: [ReAct Agent]use a re-act agent with search tool to find the linkedin url from the given name
    linkedin_url = lookup(name)
    # step 2: [No LLM, Scrape] use scrapin api to find page content from the linkedin url
    linkedin_data = scrape_linkedin_profile(linkedin_url)

    # step 3: [LLM]
    template_value = """
    given the Linkedin information {information} of a person, provide:
    1. a short introduction
    2. two interesting facts about him
    """

    template = PromptTemplate(
        name="introduction", input_variables=["information"], template=template_value
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    # option 1: call LLM directly and parse the result with StrOutputParser
    res_direct = llm.invoke(template.format_prompt(information=linkedin_data))
    print(StrOutputParser().invoke(res_direct))

    # option 2: use langchain
    chain = template | llm | StrOutputParser()
    res = chain.invoke(input={"information": linkedin_data})

    return res


if __name__ == "__main__":
    result = ice_break_with("alexkaizhang")

    print(result)
