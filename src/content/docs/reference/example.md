---
title: Reference
---

# Reference Guide

Reference pages provide a concise overview of how the Discord AI Bot works and the main settings available in the project.

## Core Components

| Component | Purpose |
|---|---|
| `Discord_bot.py` | Main Python script |
| Ollama | Runs the local AI model |
| Playwright | Controls the browser interface |
| Chromium | Browser used by Playwright |
| `requirements.txt` | Python dependencies |

## AI Model

The bot uses Ollama to generate responses.

The default model configured in the script is:

```python
model='qwen2.5:14b'
```

The model can be changed to another Ollama model, provided that model has been installed locally.

Example:

```bash
ollama pull qwen2.5:7b
```

Then update the model name in `Discord_bot.py`.

## Blacklist

The `BLACKLIST` variable contains usernames or words that should be filtered.

```python
BLACKLIST = ["yo"]
```

Multiple entries can be specified:

```python
BLACKLIST = ["example", "ExampleUser", "AnotherUser"]
```

The blacklist is checked when processing usernames and generated responses.

## Mention Blacklist

The `MENTION_BLACKLIST` variable controls which users should not be automatically mentioned.

```python
MENTION_BLACKLIST = ["yes", "bro"]
```

Users on this list can still receive responses, but the automatic mention is skipped.

## AI Personality

The normal AI behavior is controlled by the `system_prompt`.

The default personality is designed to be:

- Knowledgeable about technology
- Familiar with Windows, Linux, macOS, hardware, and scripting
- Short and conversational
- Helpful and technically focused
- Occasionally sarcastic

The system prompt can be edited directly in `Discord_bot.py` to customize the bot's personality.

## Fourth-Wall Roast Mode

The bot includes a random fourth-wall roast mode.

The default probability is:

```python
is_roast = random.random() < 0.25
```

This gives approximately a 25% chance of triggering roast mode.

Common values:

| Value | Approximate probability |
|---:|---:|
| `0.10` | 10% |
| `0.25` | 25% |
| `0.50` | 50% |
| `0.75` | 75% |

The roast target is configured separately:

```python
target_user_to_tag = "exampleuser"
```

## Link Detection

The bot checks messages for URLs using:

```python
url_match = re.search(r'(https?://[^\s]+)', latest_message)
```

When a URL is detected, the script attempts to open the page and extract its visible text.

The extracted page content is limited by:

```python
page_text_clean = " ".join(raw_text.split())[:1500]
```

The `1500` value controls the maximum number of characters included in the AI prompt.

## Response Processing

Generated responses are cleaned before being sent.

Quotation marks are removed with:

```python
reply_text = reply_text.replace('"', '').replace("'", '')
```

The generated response is also checked against the configured blacklist.

Blacklisted words are replaced with:

```text
the user
```

## Dependencies

The project uses Python packages including:

```text
ollama
playwright
```

Python's built-in modules `asyncio`, `random`, and `re` are also used.

Install dependencies with:

```bash
pip install -r requirements.txt
```

Install Playwright's Chromium browser with:

```bash
playwright install chromium
```

## Runtime

The main script is started with:

```bash
python Discord_bot.py
```

The selected Ollama model must be installed before starting the application.

## Security

Never commit passwords, API keys, authentication tokens, session cookies, or other private credentials to GitHub.

Sensitive configuration should be stored using environment variables or another secure method.
