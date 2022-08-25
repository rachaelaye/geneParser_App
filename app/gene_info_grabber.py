from datetime import datetime

import requests

SERVER = "https://rest.ensembl.org"
ENDPOINT = "/lookup/id/{}?expand=1"


class GeneInfoGrabber():
    """ Utility class to grab information about a given ensembl gene ID

    The class will be instantiated with a gene id, make a call to the ensembl
    REST API, and then process the response into a dictionary which contains the
    necessary information for RA's database.

    Attributes:
        gene_id (str): the Ensembl Gene ID for which to fetch information
        ensembl_response (dict): information returned from Ensembl about gene
        processed_info (dict): info parsed into a format for use in database
    """

    def __init__(self, gene_id: str):
        self.gene_id = gene_id
        self.ensembl_response = None
        self.processed_info = None
        self.grab_gene_info()

    @property
    def gene_info(self):
        return self.processed_info

    def grab_gene_info(self):
        self.ensembl_response = self.poll_api()
        self.processed_info = self.process_response()

    def poll_api(self) -> dict:
        """Make the query to the Ensembl REST API for the given gene ID
        """
        url = SERVER + ENDPOINT.format(self.gene_id)
        headers = {"Content-Type": "application/json"}
        request = requests.get(url, headers=headers)

        # handle bad request
        if not request.ok:
            request.raise_for_status()

        return request.json()

    def process_response(self):
        """Turn the ensembl query response into a format for adding to the DB
        """
        data = self.ensembl_response
        processed_data = {
            "search_timestamp": datetime.now(),
            "gene_id": self.gene_id,
            "gene_symbol": data["display_name"],
            "strand": '-' if data["strand"] == -1 else '+',
            "chromosome": data["seq_region_name"],
            "transcripts": [{
                "transcript_id": transcript["id"],
                "coding": True if transcript["biotype"] == "protein_coding" else False,
                "start": transcript["start"],
                "stop": transcript["end"],
                "exons": [{
                    "start": exon["start"],
                    "end": exon["end"]
                } for exon in transcript["Exon"]]
            } for transcript in data["Transcript"]],
        }

        return processed_data