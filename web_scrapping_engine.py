from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader
from IPython.display import Markdown, display
from llama_index.core.tools import FunctionTool
import logging
import sys
import os


def web_scrapper():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    # NOTE: the html_to_text=True option requires html2text to be installed

    documents = SimpleWebPageReader(html_to_text=True).load_data(
        ["http://paulgraham.com/worked.html"]
    )

    documents[0]

    index = SummaryIndex.from_documents(documents)

    # set Logging to DEBUG for more detailed outputs
    query_engine = index.as_query_engine()
    response = query_engine.query("What did the author do growing up?")

    print(display(Markdown(f"<b>{response}</b>")))

    return "Answer displayed"

web_scrapping_engine = FunctionTool.from_defaults(
    fn=web_scrapper,
    name="web_scrapper",
    description="this tool can read a website and return a markdown to the user",
)
