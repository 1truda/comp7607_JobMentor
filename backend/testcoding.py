import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "给你一个字符串 s，找到 s 中最长的 回文子串。"}
    ]
)



print(message.content)
