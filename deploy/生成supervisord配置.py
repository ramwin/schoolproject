#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


"""生成supervisor配置文件"""


from pathlib import Path

from jinja2 import Template


USER = "wangx"
ROTATE_LOG_FILE = {
    "stdout_logfile_maxbytes": "40MB",
    "stdout_logfile_backups": "3",
    "stderr_logfile_maxbytes": "40MB",
    "stderr_logfile_backups": "3",
}
RESTART_CONFIG = {
        "autostart": "true",
        "autorestart": "true",
        "startretries": "3",
}
ENVIRONMENT = (
    "PATH=\""
    f"/home/{USER}/.local/bin"
    f":/home/{USER}/node/bin/"
    f":/home/{USER}/venv/bin/"
    "\""
)

BASE_CONFIG = {
    **ROTATE_LOG_FILE,
    **RESTART_CONFIG,
    **{
        "redirect_stderr": "false",
        "user": USER,
        "environment": ENVIRONMENT,
    },
}
DJANGO_DIRECTORY = Path("/home/wangx/schoolproject/")


DJANGO_COMMANDS = [
        "test_log",
]
PROGRAMS = [
    *[
        {
            "name": django_command,
            "config": {
                "command": f"python3 manage.py {django_command}",
                "directory": DJANGO_DIRECTORY,
                **BASE_CONFIG,
            },
        }
        for django_command in DJANGO_COMMANDS
    ],
]


template = Template((
    "{% for program in PROGRAMS%}"
    "[program:{{program.name}}]\n"
        "{% for key, value in program.config.items() %}"
            "{{key}}={{value}}\n"
        "{% endfor %}"
        "stdout_logfile={{program.config.directory}}/log/{{program.name}}/supervisor/stdout.log\n"
        "stderr_logfile={{program.config.directory}}/log/{{program.name}}/supervisor/stderr.log\n"
    "\n\n"
    "{% endfor %}"
))


def main():
    """生成supervisor配置文件"""
    with open("django_commands.conf", "w", encoding="utf8") as f:
        f.write(template.render({"PROGRAMS": PROGRAMS}))


if __name__ == "__main__":
    main()
