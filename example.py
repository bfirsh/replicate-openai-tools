from openai import OpenAI
from replicate_tools import Tools

client = OpenAI()
tools = Tools(["bfirsh/weather"])

messages = [{"role": "user", "content": "What's the weather in San Francisco?"}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools.tools,
    tool_choice="required"
)

messages.extend(tools.run(response))

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
)

print(response.choices[0].message.content)
# The current weather in San Francisco is partly cloudy with a temperature of 18°C (64°F). The wind is coming from the northwest at 4 km/h (2 mph). The humidity is 58%, and there is no precipitation. The pressure is 1019 mb (30 inches), and visibility is 16 km (9 miles).
