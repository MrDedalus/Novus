import logging
from typing import Dict, List
import yaml
from flask import Flask, request, jsonify, render_template
from database import Database, DatabaseError
from models import DPIA, DPIAConversation
import openai

logging.basicConfig(level=logging.INFO)

app = Flask(name) 
@app.route("/static/dpia-form.html")
def serve_dpia_form():
    return app.send_static_file("dpia-form.html")

def load_config(config_file: str) -> dict:
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except (FileNotFoundError, IOError) as error:
        logging.error(f"Error while loading the config file: {error}")
        raise ValueError(f"Error while loading the config file: {error}")

def load_dpias_from_database(database: Database, database_config: Dict) -> List[DPIA]:
    database.fetch_dpias()
    return list(database.dpias.values())

def prepare_dataset(dpias: List[DPIA]) -> List[Dict[str, str]]:
    dataset: List[Dict[str, str]] = []
    for dpia in dpias:
        for conversation in dpia.conversations:
            input_text = f"DPIA ID: {dpia.dpia_id}\nQuestion: {conversation.question}\n"
            output_text = conversation.response
            dataset.append({"input": input_text, "output": output_text})
    return dataset

def fine_tune_model(dataset: List[Dict[str, str]]) -> None:
    # Fine-tune the language model using the dataset
    training_data = [f"{data['input']}\nResponse: {data['output']}" for data in dataset]
    openai.create("text-davinci-003", training_data=training_data, name="dpia_model")

class OpenAI:
    def __init__(self, config: Dict):
        self.config = config
        self.api_key = config.get('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')
        openai.api_key = self.api_key
        self.model_id = None

    def complete(self, prompt: str, max_tokens: int) -> str:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()

    @classmethod
    def from_config(cls, config: Dict) -> 'OpenAI':
        instance = cls(config)
        instance.model_id = config.get('openai_model_id')
        return instance

@app.route("/conversation", methods=["POST"])
def add_conversation(config):
    database_config = load_config("database_config.yml")
    database = Database.from_config(database_config)
    try:
        data = request.get_json()
        dpia_id = data.get('dpia_id')
        question = data.get('question')
        response = data.get('response')

        database.add_conversation(dpia_id, question, response)

        return jsonify({"message": "Conversation added successfully."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except DatabaseError:
        return jsonify({"error": "Database error occurred."}), 500

@app.route("/conversation", methods=["PUT"])
def update_conversation(config):
    database_config = load_config("database_config.yml")
    database = Database.from_config(database_config)
    try:
        data = request.get_json()
        dpia_id = data.get('dpia_id')
        question = data.get('question')
        new_response = data.get('response')

        database.update_conversation(dpia_id, question, new_response)

        return jsonify({"message": "Conversation updated successfully."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except DatabaseError:
        return jsonify({"error": "Database error occurred."}), 500

@app.route("/dpia-form")
def dpia_form():
    return render_template("dpia-form.html")

if __name__ == "__main__":
    app.run()
