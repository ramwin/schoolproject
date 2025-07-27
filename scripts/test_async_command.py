#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>

"""
测试异步命令的脚本
"""

import os
import sys
import django
import json
import time

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolproject.settings')
django.setup()

from django_redis import get_redis_connection


def add_test_tasks():
    """向Redis添加测试任务"""
    redis_client = get_redis_connection("default")
    
    # 添加一些测试任务
    test_tasks = [
        {
            "type": "email",
            "data": {
                "to": "test@example.com",
                "subject": "测试邮件",
                "body": "这是一个测试邮件"
            }
        },
        {
            "type": "file_process",
            "data": {
                "file_path": "/tmp/test.txt",
                "operation": "compress"
            }
        },
        {
            "type": "unknown",
            "data": {
                "message": "这是一个未知类型的任务"
            }
        }
    ]
    
    for task in test_tasks:
        redis_client.lpush("async_tasks", json.dumps(task))
        print(f"已添加任务: {task}")
    
    print(f"Redis列表 async_tasks 当前长度: {redis_client.llen('async_tasks')}")


def clear_test_tasks():
    """清空测试任务"""
    redis_client = get_redis_connection("default")
    redis_client.delete("async_tasks")
    print("已清空测试任务")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="测试异步命令")
    parser.add_argument("--action", choices=["add", "clear"], default="add", 
                       help="操作类型: add(添加任务) 或 clear(清空任务)")
    
    args = parser.parse_args()
    
    if args.action == "add":
        add_test_tasks()
    elif args.action == "clear":
        clear_test_tasks() 
