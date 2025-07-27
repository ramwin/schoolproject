#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import asyncio
import json
import logging
from typing import Any, Dict, Optional, Set

from django.core.management.base import BaseCommand
from django_redis import get_redis_connection
import redis.asyncio as redis


LOGGER = logging.getLogger(__name__)


async def async_handle(data: Dict[str, Any]) -> None:
    """
    异步处理函数，处理从Redis获取的任务数据
    
    Args:
        data: 从Redis获取的任务数据字典
    """
    LOGGER.info(f"开始处理任务: {data}")
    
    # 这里可以根据实际需求处理数据
    # 例如：发送邮件、处理文件、调用API等
    task_type = data.get('type', 'unknown')
    task_data = data.get('data', {})
    
    if task_type == 'email':
        LOGGER.info(f"处理邮件任务: {task_data}")
        # 模拟邮件发送
        await asyncio.sleep(1)
    elif task_type == 'file_process':
        LOGGER.info(f"处理文件任务: {task_data}")
        # 模拟文件处理
        await asyncio.sleep(2)
    elif task_type == 'fast_task':
        LOGGER.info(f"处理快速任务: {task_data}")
        # 模拟快速处理
        await asyncio.sleep(0.5)
    elif task_type == 'medium_task':
        LOGGER.info(f"处理中等任务: {task_data}")
        # 模拟中等处理
        await asyncio.sleep(1.0)
    elif task_type == 'slow_task':
        LOGGER.info(f"处理慢任务: {task_data}")
        # 模拟慢处理
        await asyncio.sleep(2.0)
    else:
        LOGGER.info(f"处理未知类型任务: {task_data}")
        await asyncio.sleep(0.5)
    
    LOGGER.info(f"任务处理完成: {data}")


class Command(BaseCommand):
    help = '异步处理Redis中的任务队列（支持并发处理）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--redis-key',
            type=str,
            default='async_tasks',
            help='Redis列表的键名 (默认: async_tasks)'
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=1,
            help='轮询间隔秒数 (默认: 1秒)'
        )
        parser.add_argument(
            '--max-tasks',
            type=int,
            default=None,
            help='最大处理任务数量 (默认: 无限制)'
        )
        parser.add_argument(
            '--max-concurrent',
            type=int,
            default=5,
            help='最大并发任务数量 (默认: 5个)'
        )

    async def process_tasks_concurrent(self, redis_client, redis_key: str, max_tasks: Optional[int] = None, max_concurrent: int = 5):
        """
        并发处理Redis中的任务
        
        Args:
            redis_client: Redis客户端
            redis_key: Redis列表键名
            max_tasks: 最大处理任务数量
            max_concurrent: 最大并发任务数量
        """
        processed_count = 0
        running_tasks: Set[asyncio.Task] = set()
        
        while True:
            try:
                # 清理已完成的任务
                running_tasks = {task for task in running_tasks if not task.done()}
                
                # 检查是否达到最大任务数量
                if max_tasks and processed_count >= max_tasks:
                    LOGGER.info(f"已达到最大任务数量 {max_tasks}，停止处理")
                    break
                
                # 检查是否达到最大并发数量
                if len(running_tasks) >= max_concurrent:
                    LOGGER.debug(f"当前运行任务数: {len(running_tasks)}，等待任务完成...")
                    # 等待至少一个任务完成
                    if running_tasks:
                        done, pending = await asyncio.wait(
                            running_tasks, 
                            return_when=asyncio.FIRST_COMPLETED
                        )
                        # 处理完成的任务
                        for task in done:
                            try:
                                await task
                            except Exception as e:
                                LOGGER.error(f"任务执行失败: {e}")
                        continue
                    else:
                        await asyncio.sleep(0.1)
                        continue
                
                # 尝试获取新任务
                task_data = await redis_client.rpop(redis_key)
                
                if task_data is None:
                    # 没有任务，等待一段时间后继续
                    if running_tasks:
                        LOGGER.debug(f"Redis列表 {redis_key} 为空，等待 {len(running_tasks)} 个运行中的任务完成...")
                        # 等待所有运行中的任务完成
                        await asyncio.gather(*running_tasks, return_exceptions=True)
                        running_tasks.clear()
                    else:
                        LOGGER.debug(f"Redis列表 {redis_key} 为空，等待新任务...")
                        await asyncio.sleep(1)
                    continue
                
                # 解析任务数据
                try:
                    task = json.loads(task_data.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    LOGGER.error(f"解析任务数据失败: {task_data}, 错误: {e}")
                    continue
                
                # 创建异步任务并添加到运行集合
                async def process_single_task(task_data: Dict[str, Any], task_id: int):
                    """处理单个任务的包装函数"""
                    try:
                        await async_handle(task_data)
                        LOGGER.info(f"成功处理任务 #{task_id}")
                    except Exception as e:
                        LOGGER.error(f"处理任务 #{task_id} 失败: {task_data}, 错误: {e}")
                
                processed_count += 1
                task_obj = asyncio.create_task(
                    process_single_task(task, processed_count),
                    name=f"task_{processed_count}"
                )
                running_tasks.add(task_obj)
                
                LOGGER.info(f"启动并发任务 #{processed_count}，当前运行任务数: {len(running_tasks)}")
                    
            except Exception as e:
                LOGGER.error(f"处理Redis任务时发生错误: {e}")
                await asyncio.sleep(5)  # 发生错误时等待更长时间
        
        # 等待所有剩余的任务完成
        if running_tasks:
            LOGGER.info(f"等待 {len(running_tasks)} 个剩余任务完成...")
            await asyncio.gather(*running_tasks, return_exceptions=True)

    async def async_handle(self, *args, **options):
        """
        异步处理主函数
        """
        redis_key = options['redis_key']
        interval = options['interval']
        max_tasks = options['max_tasks']
        max_concurrent = options['max_concurrent']
        
        LOGGER.info(f"启动并发异步任务处理器")
        LOGGER.info(f"Redis键: {redis_key}")
        LOGGER.info(f"轮询间隔: {interval}秒")
        LOGGER.info(f"最大并发数: {max_concurrent}")
        if max_tasks:
            LOGGER.info(f"最大任务数: {max_tasks}")
        
        # 获取Redis连接
        redis_client = get_redis_connection("default")
        
        try:
            await self.process_tasks_concurrent(redis_client, redis_key, max_tasks, max_concurrent)
        except KeyboardInterrupt:
            LOGGER.info("收到中断信号，正在停止...")
        except Exception as e:
            LOGGER.error(f"异步任务处理器发生错误: {e}")
        finally:
            LOGGER.info("异步任务处理器已停止")

    def handle(self, *args, **options):
        """
        同步入口点，启动异步事件循环
        """
        try:
            asyncio.run(self.async_handle(*args, **options))
        except KeyboardInterrupt:
            LOGGER.info("命令被用户中断")
        except Exception as e:
            LOGGER.error(f"命令执行失败: {e}")
            raise
