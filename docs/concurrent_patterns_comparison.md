# 异步并发控制模式对比

## 概述

在实现异步任务处理时，有多种并发控制模式可供选择。本文档对比了三种不同的实现方式，从简单到复杂，从丑陋到优雅。

## 实现方式对比

### 1. 手动管理Set（丑陋版本）

**文件**: `school/management/commands/async_command.py`

```python
# 丑陋的手动管理
running_tasks: Set[asyncio.Task] = set()

# 手动添加任务
task_obj = asyncio.create_task(process_single_task(task, processed_count))
running_tasks.add(task_obj)

# 手动清理完成的任务
running_tasks = {task for task in running_tasks if not task.done()}

# 手动等待任务完成
await asyncio.gather(*running_tasks, return_exceptions=True)
```

**优点**:
- 实现简单，容易理解
- 可以精确控制每个任务

**缺点**:
- 代码丑陋，手动管理复杂
- 容易出错，忘记清理任务
- 不符合Python的优雅风格

### 2. 使用Semaphore + 批处理（改进版本）

**文件**: `school/management/commands/async_command.py` (更新后)

```python
class AsyncTaskProcessor:
    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_task(self, task_data: Dict[str, Any]) -> None:
        async with self.semaphore:
            await async_handle(task_data)
    
    async def process_tasks_batch(self, tasks: list) -> None:
        task_coros = [self.process_task(task) for task in tasks]
        await asyncio.gather(*task_coros, return_exceptions=True)
```

**优点**:
- 使用信号量控制并发，更优雅
- 批处理提高效率
- 代码结构更清晰

**缺点**:
- 仍然需要手动管理批次
- 不够灵活

### 3. 生产者-消费者模式（优雅版本）

**文件**: `school/management/commands/async_command_v2.py`

```python
@asynccontextmanager
async def concurrent_worker_pool(max_workers: int):
    semaphore = asyncio.Semaphore(max_workers)
    task_queue = asyncio.Queue()
    
    async def worker(task_queue: asyncio.Queue, worker_id: int):
        while True:
            task_data = await task_queue.get()
            if task_data is None:
                break
            async with semaphore:
                await async_handle(task_data)
            task_queue.task_done()
    
    # 创建工作线程
    workers = [asyncio.create_task(worker(task_queue, i + 1)) 
               for i in range(max_workers)]
    
    try:
        yield task_queue
    finally:
        # 优雅关闭
        for _ in range(max_workers):
            await task_queue.put(None)
        await asyncio.gather(*workers, return_exceptions=True)
```

**优点**:
- 使用上下文管理器，非常优雅
- 生产者-消费者模式，经典设计
- 自动管理工作线程生命周期
- 代码结构清晰，易于维护

**缺点**:
- 实现相对复杂
- 需要理解异步上下文管理器

### 4. 使用TaskGroup（现代版本）

**文件**: `school/management/commands/async_command_v3.py`

```python
async def process_with_task_group(self, redis_client, redis_key: str, 
                                max_tasks: Optional[int] = None, 
                                max_concurrent: int = 5):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_single_task(task_data: Dict[str, Any], task_id: int):
        async with semaphore:
            await async_handle(task_data)
    
    # 使用TaskGroup（Python 3.11+）
    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            process_single_task(task, processed_count),
            name=f"task_{processed_count}"
        )
```

**优点**:
- Python 3.11+ 官方推荐的方式
- 自动管理任务生命周期
- 异常处理更优雅
- 代码最简洁

**缺点**:
- 需要Python 3.11+
- 相对较新，文档较少

## 推荐使用场景

### 1. 简单场景
- **推荐**: Semaphore + 批处理
- **原因**: 实现简单，易于理解和维护

### 2. 生产环境
- **推荐**: 生产者-消费者模式
- **原因**: 稳定可靠，易于扩展和监控

### 3. 现代项目（Python 3.11+）
- **推荐**: TaskGroup
- **原因**: 官方推荐，代码最优雅

### 4. 学习/原型
- **推荐**: 手动管理Set
- **原因**: 帮助理解底层原理

## 性能对比

| 实现方式 | 代码优雅度 | 性能 | 可维护性 | 学习成本 |
|---------|-----------|------|----------|----------|
| 手动管理Set | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Semaphore + 批处理 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| 生产者-消费者 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| TaskGroup | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

## 最佳实践建议

### 1. 选择合适的方式
- **小项目**: 使用Semaphore + 批处理
- **大项目**: 使用生产者-消费者模式
- **新项目**: 考虑TaskGroup（如果支持Python 3.11+）

### 2. 错误处理
```python
# 好的错误处理
try:
    await async_handle(task_data)
except Exception as e:
    LOGGER.error(f"任务处理失败: {e}")
    # 可以选择重试或记录到死信队列
```

### 3. 监控和日志
```python
# 添加监控指标
processed_count += 1
current_concurrent = max_concurrent - semaphore._value
LOGGER.info(f"任务 #{processed_count}，当前并发: {current_concurrent}")
```

### 4. 优雅关闭
```python
# 确保所有任务完成
await task_queue.join()  # 等待队列清空
await asyncio.gather(*workers, return_exceptions=True)  # 等待工作线程
```

## 总结

从"丑陋"到"优雅"的演进：

1. **手动管理Set** → 理解原理
2. **Semaphore + 批处理** → 改进实现
3. **生产者-消费者** → 优雅设计
4. **TaskGroup** → 现代方式

选择哪种方式取决于：
- 项目规模和复杂度
- 团队的技术水平
- Python版本要求
- 性能要求

无论选择哪种方式，都要确保：
- 正确的错误处理
- 优雅的资源管理
- 清晰的日志记录
- 适当的监控指标 
