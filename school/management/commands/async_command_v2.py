#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import asyncio
import json
import logging
from typing import Any, Dict, Optional
from contextlib import asynccontextmanager

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


@asynccontextmanager
async def concurrent_worker_pool(max_workers: int):
    """
    并发工作池上下文管理器
    
    Args:
        max_workers: 最大工作线程数
    """
    semaphore = asyncio.Semaphore(max_workers)
    
    async def worker(task_queue: asyncio.Queue, worker_id: int):
        """工作线程函数"""
        while True:
            try:
                # 从队列获取任务
                task_data = await task_queue.get()
                
                # 检查结束信号
                if task_data is None:
                    LOGGER.debug(f"工作线程 {worker_id} 收到结束信号")
                    break
                
                # 使用信号量控制并发
                async with semaphore:
                    try:
                        await async_handle(task_data)
                        LOGGER.info(f"工作线程 {worker_id} 完成任务")
                    except Exception as e:
                        LOGGER.error(f"工作线程 {worker_id} 处理任务失败: {e}")
                    finally:
                        task_queue.task_done()
                        
            except asyncio.CancelledError:
                LOGGER.debug(f"工作线程 {worker_id} 被取消")
                break
            except Exception as e:
                LOGGER.error(f"工作线程 {worker_id} 发生错误: {e}")
    
    # 创建任务队列
    task_queue = asyncio.Queue()
    
    # 创建工作线程
    workers = []
    for i in range(max_workers):
        worker_task = asyncio.create_task(worker(task_queue, i + 1))
        workers.append(worker_task)
    
    try:
        yield task_queue
    finally:
        # 发送结束信号给所有工作线程
        for _ in range(max_workers):
            await task_queue.put(None)
        
        # 等待所有工作线程完成
        await asyncio.gather(*workers, return_exceptions=True)


class Command(BaseCommand):
    help = '优雅的异步任务处理器（使用工作池模式）'

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
            '--max-workers',
            type=int,
            default=5,
            help='最大工作线程数 (默认: 5个)'
        )

    async def producer_consumer_pattern(self, redis_client, redis_key: str, 
                                      max_tasks: Optional[int] = None, 
                                      max_workers: int = 5):
        """
        使用生产者-消费者模式处理Redis任务
        
        Args:
            redis_client: Redis客户端
            redis_key: Redis列表键名
            max_tasks: 最大处理任务数量
            max_workers: 最大工作线程数
        """
        processed_count = 0
        
        async with concurrent_worker_pool(max_workers) as task_queue:
            # 生产者：从Redis获取任务并放入队列
            async def producer():
                nonlocal processed_count
                
                while True:
                    try:
                        # 检查是否达到最大任务数量
                        if max_tasks and processed_count >= max_tasks:
                            LOGGER.info(f"已达到最大任务数量 {max_tasks}")
                            break
                        
                        # 从Redis获取任务
                        task_data = await redis_client.rpop(redis_key)
                        
                        if task_data is None:
                            # 没有任务，等待一段时间
                            await asyncio.sleep(1)
                            continue
                        
                        # 解析任务数据
                        try:
                            task = json.loads(task_data.decode('utf-8'))
                        except (json.JSONDecodeError, UnicodeDecodeError) as e:
                            LOGGER.error(f"解析任务数据失败: {task_data}, 错误: {e}")
                            continue
                        
                        # 将任务放入队列
                        await task_queue.put(task)
                        processed_count += 1
                        LOGGER.info(f"生产者添加任务 #{processed_count} 到队列")
                        
                    except Exception as e:
                        LOGGER.error(f"生产者发生错误: {e}")
                        await asyncio.sleep(5)
            
            # 启动生产者
            producer_task = asyncio.create_task(producer())
            
            try:
                # 等待生产者完成
                await producer_task
            except asyncio.CancelledError:
                LOGGER.info("收到取消信号，停止生产者")
            finally:
                # 等待队列中的所有任务处理完成
                await task_queue.join()
                LOGGER.info("所有任务处理完成")

    async def async_handle(self, *args, **options):
        """
        异步处理主函数
        """
        redis_key = options['redis_key']
        interval = options['interval']
        max_tasks = options['max_tasks']
        max_workers = options['max_workers']
        
        LOGGER.info(f"启动优雅的工作池异步任务处理器")
        LOGGER.info(f"Redis键: {redis_key}")
        LOGGER.info(f"轮询间隔: {interval}秒")
        LOGGER.info(f"最大工作线程数: {max_workers}")
        if max_tasks:
            LOGGER.info(f"最大任务数: {max_tasks}")
        
        # 获取Redis连接
        redis_client = get_redis_connection("default")
        
        try:
            await self.producer_consumer_pattern(redis_client, redis_key, max_tasks, max_workers)
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
