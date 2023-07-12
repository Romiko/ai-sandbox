# Introduction
![Langchain and VectorDB](vectordb-lang-chain.png)

Use ChatGPT API and VectorDB Lookup to personalise your results.

I recommend using [Anaconda](https://www.anaconda.com/download) to maintain python environments.

## Installation
Install [Langchain](https://github.com/hwchase17/langchain)

```
pip install langchain openai chromadb tiktoken unstructured
```
Modify `constants.env.py` to use your own [OpenAI API key](https://platform.openai.com/account/api-keys) and rename to `constants.py`.

Place your own data into `data/data.txt`.

## Example
Reading `data/data.txt` file.
```
> python chatgpt.py "what are my favourite fruits?"
Your favorite fruits are apples, bananas, and oranges.
```