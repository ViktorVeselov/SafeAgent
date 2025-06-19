# Quickstart


Follow these steps to try the demo agent.

## Installation

Install the package with the testing extras so you can run the included example and tests:
=======
Install the package with testing extras:


```bash
pip install -e .[test]
```


Set your Gemini API key in the environment:

```bash
export GEMINI_API_KEY=<your-key>
```

## Running the example

Execute the pipeline entrypoint to start a question-answering agent:
=======
Run the example pipeline:


```python
from minillm.pipeline import main as run_pipeline
run_pipeline()
```


The agent will retrieve documents, call Gemini to generate an answer and store a summary of the conversation.

Configuration values such as model name, vector index path and database credentials are controlled by environment variables. See `minillm.config.Config` for defaults.
=======
Configuration values are read from environment variables, e.g.
`GEMINI_API_KEY` for Gemini models. See `minillm.config.Config`
for the complete list of defaults.
