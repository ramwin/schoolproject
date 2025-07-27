#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>

"""
异步任务处理示例
"""

import os
import sys
import django
import json
import time
import subprocess
import threading

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolproject.settings')
django.setup()

from django_redis import get_redis_connection


def add_sample_tasks():
    """添加示例任务到Redis"""
    redis_client = get_redis_connection("default")
    
    # 示例任务列表
    sample_tasks = [
        {
            "type": "email",
            "data": {
                "to": "user1@example.com",
                "subject": "欢迎邮件",
                "body": "欢迎使用我们的服务！"
            }
        },
        {
            "type": "email",
            "data": {
                "to": "user2@example.com",
                "subject": "订单确认",
                "body": "您的订单已确认，订单号：12345"
            }
        },
        {
            "type": "file_process",
            "data": {
                "file_path": "/tmp/report.pdf",
                "operation": "compress",
                "output_path": "/tmp/report_compressed.pdf"
            }
        },
        {
            "type": "file_process",
            "data": {
                "file_path": "/tmp/data.csv",
                "operation": "convert",
                "output_format": "json"
            }
        },
        {
            "type": "unknown",
            "data": {
                "message": "这是一个自定义任务",
                "timestamp": time.time()
            }
        }
    ]
    
    print("正在添加示例任务到Redis...")
    for i, task in enumerate(sample_tasks, 1):
        redis_client.lpush("async_tasks", json.dumps(task))
        print(f"任务 {i}: {task['type']} - {task['data']}")
    
    print(f"\n已添加 {len(sample_tasks)} 个任务")
    print(f"Redis列表 async_tasks 当前长度: {redis_client.llen('async_tasks')}")


def run_async_command():
    """运行异步命令"""
    print("\n启动异步任务处理器...")
    print("按 Ctrl+C 停止命令")
    print("-" * 50)
    
    try:
        # 运行Django管理命令
        subprocess.run([
            "python", "manage.py", "async_command",
            "--redis-key", "async_tasks",
            "--interval", "1"
        ], check=True)
    except KeyboardInterrupt:
        print("\n命令已停止")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")


def monitor_tasks():
    """监控任务队列状态"""
    redis_client = get_redis_connection("default")
    
    while True:
        try:
            task_count = redis_client.llen("async_tasks")
            print(f"\r当前队列中的任务数量: {task_count}", end="", flush=True)
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n监控已停止")
            break


def main():
    """主函数"""
    print("异步任务处理示例")
    print("=" * 50)
    
    # 清空现有任务
    redis_client = get_redis_connection("default")
    redis_client.delete("async_tasks")
    print("已清空现有任务")
    
    # 添加示例任务
    add_sample_tasks()
    
    print("\n选择操作:")
    print("1. 运行异步命令处理器")
    print("2. 监控任务队列")
    print("3. 同时运行处理器和监控")
    
    choice = input("\n请输入选择 (1/2/3): ").strip()
    
    if choice == "1":
        run_async_command()
    elif choice == "2":
        monitor_tasks()
    elif choice == "3":
        # 在后台线程中运行监控
        monitor_thread = threading.Thread(target=monitor_tasks, daemon=True)
        monitor_thread.start()
        
        # 运行异步命令
        run_async_command()
    else:
        print("无效选择")


if __name__ == "__main__":
    main() 
