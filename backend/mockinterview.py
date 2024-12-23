import os
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime._exceptions import ArkAPIError

class Model:
    def __init__(self):
        pass

    def chat_completion(self, messages: list[dict]) -> str:
        """Method to be implemented by subclasses to interact with the model."""
        pass

class JobMentor(Model):
    def __init__(self):
        # Use environment variables for sensitive data
        api_key = os.getenv("ARK_API_KEY", "your_api_key_here")
        self.client = Ark(
            api_key="3709ef67-2e62-4d03-9226-ecce7a7075a1",
            timeout=120,
            max_retries=2
        )
        self.model = "ep-20241118214429-kmtqw"

    def chat_completion(self, messages: list[dict]) -> str:
        """Send messages to the JobMentor model and get a response."""
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return completion.choices[0].message.content.strip()
        except ArkAPIError as e:
            print(f"API Error: {e}")
            return "An error occurred while interacting with the model."

def model_factory(model_name: str) -> Model:
    """Return a model instance based on the model name."""
    if model_name == "JobMentor":
        return JobMentor()
    else:
        return JobMentor()  # Default to JobMentor

def start_mock_interview(model: Model, theme: str):
    """Start a mock interview based on the given theme."""
    # Initialization prompt
    messages = [
        {"role": "system", "content": (
            "你是JobMentor，一位帮用户进行模拟面试的面试官。用户希望由你担任面试的考官，对用户进行模拟面试。"
            "你的职责是根据用户的主题提出明确且单一的面试问题，等待用户回答，并根据回答反馈下一步问题。"
            "当完成10个问题后，你需要总结用户的表现并宣布面试结束。"
        )}
    ]

    print("Hiiii，我是JobMentor，可以帮你进行模拟面试！")
    print("请告诉我你想要面试的主题，我将向你提出这个主题下的面试问题。")
    print("你想要面试什么样的主题？——是JAVA，Python，还是SQL？")

    print(f"主题选择为：{theme}")

    # Add theme-specific system instruction
    messages.append({"role": "system", "content": f"面试主题是{theme}，请根据主题提出明确的面试问题。"})

    print("=== 模拟面试开始 ===")
    
    for round_num in range(1, 4):  # 10 questions in total
        # AI 提问
        question_request = messages + [
            {"role": "assistant", "content": "请提出一个与主题相关的明确且单一的问题。"}
        ]
        question = model.chat_completion(question_request)
        print(f"JobMentor（第{round_num}轮提问）：{question}")

        # 获取用户回答
        user_answer = input("你的回答：")
        messages.append({"role": "user", "content": user_answer})

        # 更新对话历史
        messages.append({"role": "assistant", "content": question})

    # AI 面试总结
    summary_request = messages + [
        {"role": "assistant", "content": "请总结用户在这3个问题中的表现，然后宣布面试结束。"}
    ]
    summary = model.chat_completion(summary_request)
    print(f"JobMentor（总结）：{summary}")

    print("=== 模拟面试结束 ===")

if __name__ == "__main__":
    # 动态选择面试主题
    theme = input("请输入面试主题（JAVA, Python, SQL）：")
    while theme not in ["JAVA", "Python", "SQL"]:
        print("无效的主题，请重新输入！")
        theme = input("请输入面试主题（JAVA, Python, SQL）：")

    model = model_factory("JobMentor")
    start_mock_interview(model, theme)
