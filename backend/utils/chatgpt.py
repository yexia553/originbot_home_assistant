import openai
import time
import os
from utils import envs
import paramiko


class ChatGPT:
    def __init__(self):
        openai.api_key = envs.API_KEY
        openai.api_base = envs.API_BASE
        openai.api_type = 'azure'
        openai.api_version = '2023-07-01-preview'
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
        prompt = """
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
        response = openai.ChatCompletion.create(
            engine=envs.ENGINE,
            messages=[
                {"role":"system","content":"你是一个机器人开发专家，请你帮助我完成一些任务"},
                {"role":"user","content": prompt}
            ],
            temperature=0.1,
            max_tokens=self.max_completion_length,
            top_p=0.95,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=None,
        )
        print(response)
        text = response['choices'][0]['message']['content']
        print(text)
        res_list = text.split("###---")
        res = res_list[1]
        # res = self.remove_leading_spaces(res)
        print(res)
        res = res.splitlines()[1:]
        res = '\n'.join(res)
        with open('/tmp/OriginBot.py', 'w') as f:
            f.write(res)
        self.run_script('/tmp/OriginBot.py')

    def run_script(self, script_path):
        """
        通过SSH把脚本上传到OriginBot服务器，并在远端执行脚本
        """
        hostname = '192.168.1.111'
        port = 22
        username = 'root'
        password = 'root'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password)

        with open(script_path, 'r') as f:
            script = f.read()
        os.remove(script_path)  # 删除本地脚本
        ssh.exec_command(f'echo "{script}" > {script_path}')
        stdin, stdout, stderr = ssh.exec_command(f'export PATH=/userdata/dev_ws/install/hobot_audio/bin:/opt/tros/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:$PATH && \
                                                    export PYTHONPATH=/userdata/dev_ws/install/originbot_linefollower/lib/python3.8/site-packages:/userdata/dev_ws/install/originbot_demo/lib/python3.8/site-packages:/userdata/dev_ws/install/originbot_msgs/lib/python3.8/site-packages:/userdata/dev_ws/install/originbot_goal_service/lib/python3.8/site-packages:/opt/tros/lib/python3.8/site-packages:$PYTHONPATH &&\
                                                    source /opt/tros/setup.bash && \
                                                    source /userdata/dev_ws/install/setup.bash && \
                                                    /usr/bin/python3 /tmp/OriginBot.py')

        ssh.close()
