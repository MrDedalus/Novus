import logging
import subprocess
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO)


class DPIA:
    def __init__(self, dpia_id: str, purpose: str, scope: str, legal_bases: List[str], categories: List[str]):
        self.dpia_id = dpia_id
        self.purpose = purpose
        self.scope = scope
        self.legal_bases = legal_bases
        self.categories = categories
        self.conversations = []

    def __repr__(self):
        return f"DPIA(dpia_id={self.dpia_id}, purpose={self.purpose}, " \
               f"scope={self.scope}, legal_bases={self.legal_bases}, categories={self.categories})"

    def add_conversation(self, question: str, response: str) -> None:
        conversation = DPIAConversation(self, question, response)
        self.conversations.append(conversation)

    def get_conversations(self) -> List['DPIAConversation']:
        return self.conversations

    def update_conversation(self, question: str, new_response: str) -> None:
        for conversation in self.conversations:
            if conversation.question == question:
                conversation.response = new_response
                break

    def generate_report(self) -> None:
        """Generates a report for the DPIA."""
        try:
            subprocess.run(["./report_script.sh", self.dpia_id], check=True)
            logging.info(f"Report for DPIA {self.dpia_id} generated successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Report generation for DPIA {self.dpia_id} failed with error: {e}")


class DPIAConversation:
    def __init__(self, dpia: DPIA, question: str, response: str):
        self.dpia = dpia
        self.question = question
        self.response = response

    def __repr__(self):
        return f"DPIAConversation(dpia_id={self.dpia.dpia_id}, question={self.question}, " \
               f"response={self.response})"
