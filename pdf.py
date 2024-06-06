import os
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings

text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=0.25)

Settings.text_splitter = text_splitter

def get_index(data, index_name):
    
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)
        
        index = VectorStoreIndex.from_documents(
    data, transformations=[text_splitter]
)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index


pdf_path = os.path.join("data", "nbg-esg-report-2022-en.pdf")
nbg_pdf = PDFReader().load_data(file=pdf_path)
nbg_index = get_index(nbg_pdf, "nbg")
nbg_engine = nbg_index.as_query_engine()
