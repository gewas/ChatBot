# ChatBot
A ChatBot powered by ChatGPT and Auzre Speech Services.

## Usage

```bash
python chatbot.py
```

And follow the hints to **install the essential libs**.

At the beginning of **chatbot.py**, you should fill in your own API KEYS stuff [and proxy options].

```python
import os
# if you can't connect to openai, you may need to set your proxy options
os.environ["http_proxy"] = "http://127.0.0.1:8888"
os.environ["https_proxy"] = "http://127.0.0.1:8888"

# set the Azure Speech Service KEY and REGION
os.environ["SPEECH_KEY"] = ""
os.environ["SPEECH_REGION"] = ""

import openai

# set the openai ORG and KEY
openai.organization = ""
openai.api_key = ""
```