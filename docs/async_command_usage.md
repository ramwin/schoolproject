# 异步任务处理命令使用说明

## 概述

这个Django命令可以异步处理存储在Redis列表中的任务。它会持续监听Redis中的`async_tasks`列表，获取任务数据并执行`async_handle`函数。

## 功能特性

- 异步处理Redis列表中的任务
- 支持自定义Redis键名
- 可配置轮询间隔
- 支持最大任务数量限制
- 错误处理和日志记录
- 优雅的停止机制

## 使用方法

### 基本用法

```bash
# 使用默认设置启动异步任务处理器
python manage.py async_command

# 指定Redis键名
python manage.py async_command --redis-key my_tasks

# 设置轮询间隔为2秒
python manage.py async_command --interval 2

# 限制最大处理任务数量为100
python manage.py async_command --max-tasks 100

# 组合使用
python manage.py async_command --redis-key my_tasks --interval 2 --max-tasks 100
```

### 参数说明

- `--redis-key`: Redis列表的键名，默认为 `async_tasks`
- `--interval`: 轮询间隔秒数，默认为 1 秒
- `--max-tasks`: 最大处理任务数量，默认为无限制

## 任务数据格式

任务数据应该是JSON格式的字典，包含以下字段：

```json
{
    "type": "email",
    "data": {
        "to": "user@example.com",
        "subject": "邮件主题",
        "body": "邮件内容"
    }
}
```

### 支持的任务类型

1. **email**: 邮件任务
2. **file_process**: 文件处理任务
3. **unknown**: 未知类型任务（默认处理）

## 测试

### 添加测试任务

```bash
# 添加测试任务到Redis
python scripts/test_async_command.py --action add

# 清空测试任务
python scripts/test_async_command.py --action clear
```

### 运行命令测试

```bash
# 1. 首先添加一些测试任务
python scripts/test_async_command.py --action add

# 2. 启动异步命令处理器
python manage.py async_command

# 3. 观察日志输出，查看任务处理情况
```

## 日志输出示例

```
2024-01-01 10:00:00 INFO 启动异步任务处理器
2024-01-01 10:00:00 INFO Redis键: async_tasks
2024-01-01 10:00:00 INFO 轮询间隔: 1秒
2024-01-01 10:00:01 INFO 开始处理任务: {'type': 'email', 'data': {...}}
2024-01-01 10:00:01 INFO 处理邮件任务: {...}
2024-01-01 10:00:02 INFO 任务处理完成: {'type': 'email', 'data': {...}}
2024-01-01 10:00:02 INFO 成功处理任务 #1
```

## 自定义处理逻辑

你可以修改 `async_handle` 函数来实现自己的任务处理逻辑：

```python
async def async_handle(data: Dict[str, Any]) -> None:
    """
    自定义任务处理逻辑
    """
    task_type = data.get('type')
    task_data = data.get('data', {})
    
    if task_type == 'custom_task':
        # 处理自定义任务
        await process_custom_task(task_data)
    elif task_type == 'api_call':
        # 处理API调用任务
        await call_external_api(task_data)
    else:
        # 处理其他任务类型
        await process_default_task(task_data)
```

## 注意事项

1. 确保Redis服务正在运行
2. 任务数据必须是有效的JSON格式
3. 处理失败的任务不会自动重试
4. 使用 `Ctrl+C` 可以优雅地停止命令
5. 建议在生产环境中使用进程管理器（如supervisor）来运行此命令

## 错误处理

- 如果Redis连接失败，命令会记录错误并退出
- 如果任务数据格式无效，会跳过该任务并继续处理下一个
- 如果任务处理过程中发生异常，会记录错误但不会停止整个进程 
