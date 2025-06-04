# woodworkers_rag_assistant

An interactive system that allows users to ask natural-language questions about woodworking, and get accurate answers grounded in open-source woodworking literature.

## Corpus

See https://github.com/thomaspurk/woodworking_corpus

## Development Environment

|               |                        |
| ------------- | ---------------------- |
| Platform      | OS MacOS Sonoma 14.7.4 |
| IDE           | VS Code 1.100.2        |
| Runtime       | Python 3.13.1          |
| Documentation | Markdown / DocString   |
| Unit Testing  | PyTest                 |
| Repository    | GitHub.com             |

### Setup

1. Clone the GitHub repository

2. Create a virtual Python Environment.
   <br>NOTE: The .venv folder is listed in the .gitignore file.

```shell
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

3. Create a .env.development.local file. See the file template.env.development.local for required variables.
   <br>NOTE: The .env.development.local file is listed in the .gitignore file.

## Processing

1. Load Corpus Into Vector Store - execute "src/data_loaders/load_corpus.py"
2. Verify Vector Store Content - execute "src/data_loaders/validate_vectore_store.py"
