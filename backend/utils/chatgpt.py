import openai
import time
import os
from utils import envs
import subprocess


class ChatGPT:
    def __init__(self):
        openai.api_key = envs.API_KEY
        openai.api_base = envs.API_BASE
        openai.api_type = 'azure'
        openai.api_version = '2022-12-01'
        self.messages = []
        self.max_token_length = 6000
        self.max_completion_length = 3000
        self.last_response = None
        self.query = ''
        self.instruction = ''

    def extract_json_part(self, text):
        # because the json part is in the middle of the text, we need to extract it.
        # json part is between ``` and ```.
        # skip if there is no json part
        if text.find('```') == -1:
            return text
        text_json = text[text.find('```') + 3 : text.find('```', text.find('```') + 3)]
        return text_json

    def remove_leading_spaces(self, code, spaces=8):
        lines = code.split('\n')  # 按行分割代码
        processed_lines = [
            line[spaces:] if line.startswith(' ' * spaces) else line for line in lines
        ]  # 移除每一行开头的空格
        return '\n'.join(processed_lines)

    def generate(self, user_input):
        prompt = """[user]
        我会交给你一些信息、要求，请你完成任务。
        以下是信息：
        1. OriginBot是一个两轮的轮式机器人，基于ROS2 foxy开发
        2. 运动速度的topic是/cmd_vel
        以下是要求：
        1. 代码只能用Python
        2. 要基于rclpy.node的Node类拓展
        3. 代码中要考虑在合适的地方调用rclpy.shutdown()来销毁当前Node节点，而不是要求手动介入
        4. 线速度为0.2米/s
        5. 输出只能包含markdown格式的python代码，格式模板如下：
        ```python
        ###---
        import rclpy
        from geometry_msgs.msg import Twist
        from rclpy.node import Node


        class OriginBot(Node):
            def __init__(self):
                ...

            def xxx_function(self):
                ...

        def main(args=None):
            rclpy.init(args=args)
            originbot = OriginBot()
            rclpy.spin(originbot)
            originbot.destroy_node()
            rclpy.shutdown()

        if __name__ == '__main__':
            main()
        ###---
        ```
        代码开头和结尾的###---都必须要显示的输出，并且最后要调用main函数
        以下是任务: 
        """
        prompt += user_input
        response = openai.Completion.create(
            engine=envs.ENGINE,
            prompt=prompt,
            temperature=0.1,
            max_tokens=self.max_completion_length,
            top_p=0.95,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=None,
        )
        text = response['choices'][0]['text']
        print(text)
        res_list = text.split("###---")
        res = res_list[1]
        res = self.remove_leading_spaces(res)
        with open('/tmp/OriginBot.py', 'w') as f:
            f.write(res)
        self.run_script('/tmp/OriginBot.py')
        # time.sleep(30)
        # os.remove('OriginBot.py')

    def run_script(self, script_path):
        # Check if the script file exists.
        try:
            with open(script_path, 'r') as file:
                pass
        except IOError:
            print('The Python script does not exist.')
            return

        # Run the script.
        try:
            process = subprocess.Popen(["python3", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # If the script was executed successfully, stdout will hold its output. 
            # If there was an error executing the script, stderr will hold the error message.
            if stdout:
                print(f"Output:\n{stdout.decode()}")
            if stderr:
                print(f"Error:\n{stderr.decode()}")

        except Exception as e:
            print(f'Error occurred while running the script: {str(e)}')
