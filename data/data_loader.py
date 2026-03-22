```json
{
    "data/data_loader.py": {
        "content": "
import logging
from typing import Dict, List
from PyMuPDF import fitz
from elasticsearch import Elasticsearch
from embedchain import EmbedChain
from biasalert import BiasAlert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, es_index: str, embedchain_model: str, biasalert_model: str):
        """
        Initialize the DataLoader class.

        Args:
        - es_index (str): The Elasticsearch index to use.
        - embedchain_model (str): The EmbedChain model to use.
        - biasalert_model (str): The BiasAlert model to use.
        """
        self.es_index = es_index
        self.embedchain_model = embedchain_model
        self.biasalert_model = biasalert_model
        self.es_client = Elasticsearch()
        self.embedchain = EmbedChain(self.embedchain_model)
        self.biasalert = BiasAlert(self.biasalert_model)

    def load_non_stationary_drift_index(self, doc_id: str) -> Dict:
        """
        Load the non-stationary drift index for a given document.

        Args:
        - doc_id (str): The ID of the document.

        Returns:
        - A dictionary containing the non-stationary drift index.
        """
        try:
            doc = self.es_client.get(index=self.es_index, id=doc_id)
            non_stationary_drift_index = self.embedchain.extract_drift_index(doc['_source']['text'])
            return {'non_stationary_drift_index': non_stationary_drift_index}
        except Exception as e:
            logger.error(f'Error loading non-stationary drift index: {e}')
            return {}

    def load_stochastic_regime_switch(self, doc_id: str) -> Dict:
        """
        Load the stochastic regime switch for a given document.

        Args:
        - doc_id (str): The ID of the document.

        Returns:
        - A dictionary containing the stochastic regime switch.
        """
        try:
            doc = self.es_client.get(index=self.es_index, id=doc_id)
            stochastic_regime_switch = self.biasalert.extract_regime_switch(doc['_source']['text'])
            return {'stochastic_regime_switch': stochastic_regime_switch}
        except Exception as e:
            logger.error(f'Error loading stochastic regime switch: {e}')
            return {}

    def load_pdf_data(self, pdf_file: str) -> List:
        """
        Load data from a PDF file.

        Args:
        - pdf_file (str): The path to the PDF file.

        Returns:
        - A list of extracted text from the PDF file.
        """
        try:
            doc = fitz.open(pdf_file)
            text = []
            for page in doc:
                text.append(page.get_text())
            return text
        except Exception as e:
            logger.error(f'Error loading PDF data: {e}')
            return []

if __name__ == '__main__':
    # Simulation of the 'Rocket Science' problem
    data_loader = DataLoader('rocket_science_index', 'embedchain_model', 'biasalert_model')
    doc_id = 'rocket_science_doc'
    non_stationary_drift_index = data_loader.load_non_stationary_drift_index(doc_id)
    stochastic_regime_switch = data_loader.load_stochastic_regime_switch(doc_id)
    pdf_file = 'rocket_science_pdf.pdf'
    pdf_data = data_loader.load_pdf_data(pdf_file)
    logger.info(f'Non-stationary drift index: {non_stationary_drift_index}')
    logger.info(f'Stochastic regime switch: {stochastic_regime_switch}')
    logger.info(f'PDF data: {pdf_data}
",
        "commit_message": "feat: implement specialized data_loader logic"
    }
}
```