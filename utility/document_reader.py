import logging
import pathlib
import pandas as pd

from typing import Any

from langchain.document_loaders import (
    TextLoader,
    UnstructuredEPubLoader,
    UnstructuredWordDocumentLoader,
    PDFMinerLoader,
    DirectoryLoader
)
from langchain.schema import Document



class EpubReader(UnstructuredEPubLoader):
    def __init__(self, file_path: str | list[str], **unstructured_kwargs: Any):
        super().__init__(file_path, **unstructured_kwargs, mode="elements", strategy="fast")


class DocumentLoaderException(Exception):
    pass


class DocumentLoader(object):
    """Loads in a document with a supported extension."""
    supported_extensions = {
        ".pdf": PDFMinerLoader,
        ".txt": TextLoader,
        ".epub": EpubReader,
        ".docx": UnstructuredWordDocumentLoader,
        ".doc": UnstructuredWordDocumentLoader
    }


def load_document(temp_filepath: str) -> list[Document]:
    """Load a file and return it as a list of documents.
    """
    ext = pathlib.Path(temp_filepath).suffix
    loader = DocumentLoader.supported_extensions.get(ext)

    print(ext)
    if not loader:
        raise DocumentLoaderException(
            f"Invalid extension type {ext}, cannot load this type of file"
        )

    loaded = loader(temp_filepath)
    docs = loaded.load()
    logging.info(docs)
    return docs
