#!/bin/bash

# 异步任务处理器启动脚本

# 设置项目路径
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# 检查Redis连接
echo "检查Redis连接..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolproject.settings')
django.setup()
from django_redis import get_redis_connection
try:
    redis_client = get_redis_connection('default')
    redis_client.ping()
    print('Redis连接正常')
except Exception as e:
    print(f'Redis连接失败: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "Redis连接失败，请检查Redis服务是否运行"
    exit 1
fi

# 获取命令行参数
REDIS_KEY=${1:-"async_tasks"}
INTERVAL=${2:-1}
MAX_TASKS=${3:-""}
MAX_CONCURRENT=${4:-5}

echo "启动并发异步任务处理器..."
echo "Redis键: $REDIS_KEY"
echo "轮询间隔: ${INTERVAL}秒"
echo "最大并发数: $MAX_CONCURRENT"
if [ -n "$MAX_TASKS" ]; then
    echo "最大任务数: $MAX_TASKS"
    python manage.py async_command --redis-key "$REDIS_KEY" --interval "$INTERVAL" --max-tasks "$MAX_TASKS" --max-concurrent "$MAX_CONCURRENT"
else
    python manage.py async_command --redis-key "$REDIS_KEY" --interval "$INTERVAL" --max-concurrent "$MAX_CONCURRENT"
fi 
