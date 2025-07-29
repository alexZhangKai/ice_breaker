from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent


def ice_break_with(name: str):

    # step 1: [ReAct Agent]use a re-act agent with search tool to find the linkedin url from the given name
    linkedin_url = linkedin_lookup_agent(name)
    # step 2: [No LLM, Scrape] use scrapin api to find page content from the linkedin url
    linkedin_data = scrape_linkedin_profile(linkedin_url)

    twitter_username = twitter_lookup_agent(name)
    tweets = scrape_user_tweets(twitter_username)

    # step 3: [LLM]
    template_value = """
    given the Linkedin information {linkedin_profile},
    and twitter posts {tweets} of a person, provide:
    1. a short introduction
    2. two interesting facts about him
    """

    template = PromptTemplate(
        name="introduction",
        input_variables=["linkedin_profile", "tweets"],
        template=template_value,
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    # option 1: call LLM directly and parse the result with StrOutputParser
    res_direct = llm.invoke(
        template.format_prompt(linkedin_profile=linkedin_data, tweets=tweets)
    )
    print(StrOutputParser().invoke(res_direct))

    # option 2: use langchain
    chain = template | llm | StrOutputParser()
    res = chain.invoke(input={"linkedin_profile": linkedin_data, "tweets": tweets})

    return res


if __name__ == "__main__":
    result = ice_break_with("Eden Marco Udemy")

    print(result)
