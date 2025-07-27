#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>

"""
测试并发任务处理效果
"""

import os
import sys
import django
import json
import time
import asyncio
import threading
from datetime import datetime

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolproject.settings')
django.setup()

from django_redis import get_redis_connection


def add_concurrent_test_tasks():
    """添加并发测试任务到Redis"""
    redis_client = get_redis_connection("default")
    
    # 清空现有任务
    redis_client.delete("async_tasks")
    
    # 创建不同处理时间的测试任务
    test_tasks = []
    
    # 快速任务（0.5秒）
    for i in range(3):
        test_tasks.append({
            "type": "fast_task",
            "data": {
                "task_id": f"fast_{i+1}",
                "duration": 0.5,
                "message": f"快速任务 {i+1}"
            }
        })
    
    # 中等任务（1秒）
    for i in range(2):
        test_tasks.append({
            "type": "medium_task",
            "data": {
                "task_id": f"medium_{i+1}",
                "duration": 1.0,
                "message": f"中等任务 {i+1}"
            }
        })
    
    # 慢任务（2秒）
    for i in range(2):
        test_tasks.append({
            "type": "slow_task",
            "data": {
                "task_id": f"slow_{i+1}",
                "duration": 2.0,
                "message": f"慢任务 {i+1}"
            }
        })
    
    print("正在添加并发测试任务到Redis...")
    print(f"任务总数: {len(test_tasks)}")
    print("任务分布:")
    print("- 快速任务 (0.5秒): 3个")
    print("- 中等任务 (1秒): 2个")
    print("- 慢任务 (2秒): 2个")
    print()
    
    for i, task in enumerate(test_tasks, 1):
        redis_client.lpush("async_tasks", json.dumps(task))
        print(f"任务 {i}: {task['type']} - {task['data']['message']}")
    
    print(f"\n已添加 {len(test_tasks)} 个任务")
    print(f"Redis列表 async_tasks 当前长度: {redis_client.llen('async_tasks')}")
    print()
    print("预期行为:")
    print("- 串行处理: 总时间约 7.5 秒 (3×0.5 + 2×1 + 2×2)")
    print("- 并发处理: 总时间约 2-3 秒 (取决于并发数)")


def monitor_task_progress():
    """监控任务处理进度"""
    redis_client = get_redis_connection("default")
    start_time = time.time()
    
    print("开始监控任务处理进度...")
    print("时间戳 | 队列剩余 | 已处理 | 运行时间")
    print("-" * 50)
    
    while True:
        try:
            current_time = time.time()
            elapsed = current_time - start_time
            remaining = redis_client.llen("async_tasks")
            
            # 估算已处理的任务数（假设总共7个任务）
            processed = max(0, 7 - remaining)
            
            timestamp = datetime.fromtimestamp(current_time).strftime("%H:%M:%S")
            print(f"{timestamp} | {remaining:>8} | {processed:>6} | {elapsed:>6.1f}s", end="\r")
            
            # 如果队列为空且运行时间超过1秒，可能处理完成
            if remaining == 0 and elapsed > 1:
                print(f"\n任务处理完成！总耗时: {elapsed:.1f}秒")
                break
                
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\n监控已停止")
            break
        except Exception as e:
            print(f"\n监控出错: {e}")
            break


def run_concurrent_test():
    """运行并发测试"""
    print("=" * 60)
    print("并发任务处理测试")
    print("=" * 60)
    
    # 添加测试任务
    add_concurrent_test_tasks()
    
    print("\n选择测试模式:")
    print("1. 串行处理 (max-concurrent=1)")
    print("2. 并发处理 (max-concurrent=3)")
    print("3. 高并发处理 (max-concurrent=5)")
    print("4. 监控模式 (只监控，不启动处理器)")
    
    choice = input("\n请输入选择 (1/2/3/4): ").strip()
    
    if choice == "1":
        print("\n启动串行处理测试...")
        print("预期: 任务依次处理，总时间约7.5秒")
        os.system("python manage.py async_command --redis-key async_tasks --max-concurrent 1")
    elif choice == "2":
        print("\n启动并发处理测试...")
        print("预期: 任务并发处理，总时间约2-3秒")
        os.system("python manage.py async_command --redis-key async_tasks --max-concurrent 3")
    elif choice == "3":
        print("\n启动高并发处理测试...")
        print("预期: 任务高并发处理，总时间约2秒")
        os.system("python manage.py async_command --redis-key async_tasks --max-concurrent 5")
    elif choice == "4":
        print("\n启动监控模式...")
        monitor_task_progress()
    else:
        print("无效选择")


def compare_serial_vs_concurrent():
    """比较串行和并发处理的性能"""
    print("=" * 60)
    print("串行 vs 并发性能对比")
    print("=" * 60)
    
    # 添加测试任务
    add_concurrent_test_tasks()
    
    print("\n测试1: 串行处理 (max-concurrent=1)")
    print("按回车开始测试...")
    input()
    
    start_time = time.time()
    os.system("python manage.py async_command --redis-key async_tasks --max-concurrent 1 --max-tasks 7")
    serial_time = time.time() - start_time
    
    print(f"\n串行处理完成，耗时: {serial_time:.1f}秒")
    
    # 重新添加任务
    add_concurrent_test_tasks()
    
    print("\n测试2: 并发处理 (max-concurrent=3)")
    print("按回车开始测试...")
    input()
    
    start_time = time.time()
    os.system("python manage.py async_command --redis-key async_tasks --max-concurrent 3 --max-tasks 7")
    concurrent_time = time.time() - start_time
    
    print(f"\n并发处理完成，耗时: {concurrent_time:.1f}秒")
    
    print("\n" + "=" * 60)
    print("性能对比结果:")
    print(f"串行处理时间: {serial_time:.1f}秒")
    print(f"并发处理时间: {concurrent_time:.1f}秒")
    print(f"性能提升: {serial_time/concurrent_time:.1f}倍")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="并发任务处理测试")
    parser.add_argument("--mode", choices=["test", "compare", "monitor"], default="test",
                       help="测试模式: test(基本测试) compare(性能对比) monitor(监控)")
    
    args = parser.parse_args()
    
    if args.mode == "test":
        run_concurrent_test()
    elif args.mode == "compare":
        compare_serial_vs_concurrent()
    elif args.mode == "monitor":
        monitor_task_progress() 
