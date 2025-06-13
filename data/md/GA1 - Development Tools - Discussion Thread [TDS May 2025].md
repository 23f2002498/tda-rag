# GA1 - Development Tools - Discussion Thread [TDS May 2025]

**User**: carlton
**URL**: [https://discourse.onlinedegree.iitm.ac.in/t/ga1-development-tools-discussion-thread-tds-may-2025/173524/10](https://discourse.onlinedegree.iitm.ac.in/t/ga1-development-tools-discussion-thread-tds-may-2025/173524/10)

[@21f3000745](/u/21f3000745) [@24f1001824](/u/24f1001824)

You can get your free key from here:

![]()
[aipipe.org](https://aipipe.org/login)

### [AI Pipe | Login](https://aipipe.org/login)

It is documented here:

[github.com](https://github.com/sanand0/aipipe/)

![](https://europe1.discourse-cdn.com/flex013/uploads/iitm/optimized/3X/8/a/8a2fee3c4df6d37bcf948b255f6d2eb3ab4594a0_2_690x344.png)

### [GitHub - sanand0/aipipe: Gives anyone access to an OpenAI/OpenRouter API...](https://github.com/sanand0/aipipe/)

Gives anyone access to an OpenAI/OpenRouter API key free at 10 cents/week. Self-hostable. Useful as a backend if you're building pure front-end LLM apps

You can use the AI Pipe Token from [aipipe.org/login](http://aipipe.org/login) in any OpenAI API compatible application by setting:

OPENAI\_API\_KEY as your AI Pipe Token

OPENAI\_BASE\_URL as <https://aipipe.org/openai/v1>

eg. (in Linux BASH)

```
export OPENAI_API_KEY=your_aipipe_token_goes_here

```

```
export OPENAI_BASE_URL="https://aipipe.org/openai/v1"

```

Then if you have `uv` installed

> **Note:** ~~The tool previously named `uvx` is now `uvenv` due to a naming collision with a new `uv` command. The new name better reflects its purpose, combining `uv` with `venv` .  
> It’s been used here so that those who are familiar with `uvx` can understand the below command. It is always good practise to migrate away from deprecated tools to newer maintained ones because deprecated tools are easy targets of open-source supply chain code injection attacks.~~  
> `uvx` is not the same as the python library uvx. `uvx` here is a command within uv.

```
uvx openai api chat.completions.create -m gpt-4.1-nano -g user "Hello. Give me 5 names for a pet dog."

```

or

```
uvx llm 'Hello. What is 2 + 2?' -m gpt-4.1-nano --key $OPENAI_API_KEY

```
