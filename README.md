# Cover Letter Generator

Small, unambitious project to familiarize myself with langchain and prompting.

The objective is simple, from a summary, a LinkedIn link of a job offer (the link must be directly that of the advertisement) and other optional information, generate a cover letter.

Streamlit is used for the interface for its simplicity of implementation.
Langchain is used to vectorize our data but in reality we have quite little of it and we could do without it.

## Demo

[View Live Demo](https://easy-cover-letter-powered-by-ai.streamlit.app/)

## Quickstart

### Prerequisites
- Install packages in requirements.txt
- You need an OPEN AI Api key
- Chrome if you want to also get basic company data from linkedin (disable on demo)

### Run
```
streamlit run src/app.py
```
