# Django异步任务处理命令

## 概述

这个项目实现了一个Django管理命令，可以异步处理存储在Redis列表中的任务。命令会持续监听Redis中的任务队列，获取任务数据并执行相应的处理函数。

## 文件结构

```
schoolproject/
├── school/management/commands/
│   └── async_command.py          # 主要的异步命令实现
├── scripts/
│   ├── test_async_command.py     # 测试脚本
│   └── start_async_worker.sh     # 启动脚本
├── examples/
│   └── async_task_example.py     # 使用示例
└── docs/
    └── async_command_usage.md    # 详细使用说明
```

## 核心功能

### 1. 异步任务处理 (`async_command.py`)

- **异步处理**: 使用Python的`asyncio`实现真正的异步处理
- **Redis集成**: 从Redis列表中获取任务数据
- **错误处理**: 完善的错误处理和日志记录
- **可配置**: 支持自定义Redis键名、轮询间隔、最大任务数等参数

### 2. 任务处理函数 (`async_handle`)

支持多种任务类型：
- `email`: 邮件发送任务
- `file_process`: 文件处理任务
- `unknown`: 默认任务类型

### 3. 命令行参数

- `--redis-key`: Redis列表键名（默认: `async_tasks`）
- `--interval`: 轮询间隔秒数（默认: 1秒）
- `--max-tasks`: 最大处理任务数量（默认: 无限制）

## 快速开始

### 1. 基本使用

```bash
# 启动异步任务处理器
python manage.py async_command

# 使用自定义参数
python manage.py async_command --redis-key my_tasks --interval 2 --max-tasks 100
```

### 2. 使用启动脚本

```bash
# 使用默认设置
./scripts/start_async_worker.sh

# 自定义参数
./scripts/start_async_worker.sh my_tasks 2 100
```

### 3. 测试功能

```bash
# 添加测试任务
python scripts/test_async_command.py --action add

# 清空测试任务
python scripts/test_async_command.py --action clear

# 运行完整示例
python examples/async_task_example.py
```

## 任务数据格式

任务数据应该是JSON格式的字典：

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

## 日志输出

命令会输出详细的日志信息：

```
2024-01-01 10:00:00 INFO 启动异步任务处理器
2024-01-01 10:00:00 INFO Redis键: async_tasks
2024-01-01 10:00:00 INFO 轮询间隔: 1秒
2024-01-01 10:00:01 INFO 开始处理任务: {'type': 'email', 'data': {...}}
2024-01-01 10:00:01 INFO 处理邮件任务: {...}
2024-01-01 10:00:02 INFO 任务处理完成: {'type': 'email', 'data': {...}}
2024-01-01 10:00:02 INFO 成功处理任务 #1
```

## 自定义扩展

### 添加新的任务类型

在`async_handle`函数中添加新的任务类型处理：

```python
async def async_handle(data: Dict[str, Any]) -> None:
    task_type = data.get('type')
    task_data = data.get('data', {})
    
    if task_type == 'new_task_type':
        # 处理新任务类型
        await process_new_task(task_data)
    elif task_type == 'email':
        # 处理邮件任务
        await process_email_task(task_data)
    # ... 其他任务类型
```

### 修改处理逻辑

你可以完全自定义`async_handle`函数的实现，例如：

- 调用外部API
- 处理文件上传
- 发送通知
- 数据同步
- 等等

## 生产环境部署

### 使用Supervisor

创建supervisor配置文件：

```ini
[program:async_worker]
command=python manage.py async_command --redis-key async_tasks --interval 1
directory=/path/to/your/project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/async_worker.log
```

### 使用Docker

```dockerfile
# 在Dockerfile中添加
CMD ["python", "manage.py", "async_command"]
```

## 注意事项

1. **Redis依赖**: 确保Redis服务正在运行
2. **数据格式**: 任务数据必须是有效的JSON格式
3. **错误处理**: 处理失败的任务不会自动重试
4. **优雅停止**: 使用`Ctrl+C`可以优雅地停止命令
5. **监控**: 建议在生产环境中添加监控和告警

## 故障排除

### 常见问题

1. **Redis连接失败**
   - 检查Redis服务是否运行
   - 验证Redis连接配置

2. **任务处理失败**
   - 检查任务数据格式是否正确
   - 查看日志了解具体错误

3. **命令无法启动**
   - 检查Django环境是否正确设置
   - 验证依赖包是否已安装

### 调试技巧

```bash
# 启用详细日志
export DJANGO_LOG_LEVEL=DEBUG

# 测试Redis连接
python -c "from django_redis import get_redis_connection; redis = get_redis_connection('default'); print(redis.ping())"

# 查看Redis中的任务
python scripts/test_async_command.py --action add
```

## 贡献

欢迎提交Issue和Pull Request来改进这个异步任务处理命令！

## 许可证

本项目采用MIT许可证。 
