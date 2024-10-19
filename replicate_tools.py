import json
import replicate


class Tools:
    def __init__(self, models):
        self.models = {}
        for model_name in models:
            model = replicate.models.get(model_name)
            version = model.versions.list()[0]
            self.models[model_name.replace("/", "-")] = (model, version)

    @property
    def tools(self):
        tools = []
        for name, (model, version) in self.models.items():
            input_schema = version.openapi_schema["components"]["schemas"]["Input"]
            tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": model.description,
                    "parameters": input_schema,
                },
                "strict": True,
            })
        return tools

    def run(self, response):
        messages = [response.choices[0].message]
        for tool_call in response.choices[0].message.tool_calls:
            arguments = json.loads(tool_call.function.arguments)
            model, version = self.models[tool_call.function.name]
            output = replicate.run(version, input=arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(output),
            })
        return messages
