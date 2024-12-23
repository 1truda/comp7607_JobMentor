import os
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime._exceptions import ArkAPIError


class Model:
    """抽象基类，用于实现不同的模型"""
    def __init__(self):
        pass

    def chat_completion(self, messages: list[dict]) -> str:
        """抽象方法，子类需实现"""
        raise NotImplementedError("Subclasses must implement this method.")


class JobMentor(Model):
    """JobMentor 模型类，用于处理模拟面试逻辑"""
    def __init__(self):
        # 从环境变量中读取 API Key
        api_key = os.getenv("ARK_API_KEY", "3709ef67-2e62-4d03-9226-ecce7a7075a1")
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("API key is missing. Set ARK_API_KEY in the environment variables.")
        self.client = Ark(api_key=api_key, timeout=120, max_retries=2)
        self.model = "ep-20241118214429-kmtqw"

    def chat_completion(self, messages: list[dict]) -> str:
        """调用 JobMentor 模型生成响应"""
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return completion.choices[0].message.content.strip()
        except ArkAPIError as e:
            print(f"API Error: {e}")
            return "An error occurred while interacting with the model."
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return "An unexpected error occurred while interacting with the model."


class InterviewSession:
    """管理模拟面试会话"""
    def __init__(self, theme: str):
        if not theme:
            raise ValueError("面试主题不能为空。")
        self.theme = theme
        self.messages = [
            {"role": "system", "content": (
                "你是JobMentor，一位帮用户进行模拟面试的面试官。用户希望由你担任面试的考官，对用户进行模拟面试。"
                "你的职责是根据用户的主题提出明确且单一的面试问题，等待用户回答，并根据回答反馈下一步问题。"
                "当完成3个问题后，你需要总结用户的表现并宣布面试结束。"
            )},
            {"role": "system", "content": f"面试主题是{theme}，请根据主题提出明确的面试问题。"}
        ]
        self.completed_questions = 0  # 已完成的问题数
        self.max_questions = 3      # 最大问题数
        self.answers = []           # 用户的回答列表

    def get_next_question(self, model: JobMentor) -> str:
        """获取下一个面试问题"""
        if self.completed_questions >= self.max_questions:
            return "面试已经结束。请调用总结方法。"

        try:
            question_request = self.messages + [
                {"role": "assistant", "content": "请提出一个与主题相关的明确且单一的问题。"}
            ]
            question = model.chat_completion(question_request).strip()
            if question:
                self.messages.append({"role": "assistant", "content": question})
                self.completed_questions += 1
                return question
            else:
                raise ValueError("生成的问题为空，请检查模型响应。")
        except Exception as e:
            return f"生成问题时发生错误：{e}"

    def add_user_answer(self, answer: str):
        """记录用户的回答"""
        if not answer.strip():
            raise ValueError("用户回答不能为空。")
        self.answers.append(answer.strip())
        self.messages.append({"role": "user", "content": answer.strip()})

    def summarize_interview(self, model: JobMentor) -> str:
        """总结面试表现"""
        if self.completed_questions < self.max_questions:
            return "面试尚未完成，请完成所有问题后再总结。"

        self.messages.append(
            {"role": "assistant", "content": "请总结用户在这3个问题中的表现，然后宣布面试结束。"}
        )
        try:
            summary = model.chat_completion(self.messages).strip()
            return summary
        except Exception as e:
            return f"总结面试时发生错误：{e}"


# 确保正确导出类
__all__ = ["JobMentor", "InterviewSession"]