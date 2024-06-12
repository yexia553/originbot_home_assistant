from utils.llms import azure_gpt4o


message = [
    {
        "role": "system",
        "content": "你是一个机器人开发专家，请你帮助我完成一些任务",
    },
    {
        "role": "user",
        "content": "介绍一下自己",
    },
]

res = azure_gpt4o(message)
print(res)
