# 代码生成时间: 2025-09-24 08:10:18
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
# 优化算法效率
from starlette.routing import Route


class SystemPerformanceMonitor:
    """系统性能监控工具"""
# NOTE: 重要实现细节
    def __init__(self):
        self.cpu_usage = None
        self.memory_usage = None
        self.disk_usage = None
# 添加错误处理

    def update_usage(self):
        """更新系统使用情况"""
        self.cpu_usage = psutil.cpu_percent()
        self.memory_usage = psutil.virtual_memory().percent
# NOTE: 重要实现细节
        self.disk_usage = psutil.disk_usage('/').percent

    def get_system_usage(self):
# 优化算法效率
        """获取系统使用情况"""
        try:
            self.update_usage()
            return {
                'cpu_usage': self.cpu_usage,
                'memory_usage': self.memory_usage,
                'disk_usage': self.disk_usage
# 优化算法效率
            }
        except Exception as e:
            return {'error': str(e)}


async def system_usage_endpoint(request):
    """系统使用情况监控端点"""
    monitor = SystemPerformanceMonitor()
    usage = monitor.get_system_usage()
    return JSONResponse(usage)


def create_app():
    """创建Starlette应用"""
    return Starlette(
        routes=[
# 改进用户体验
            Route('/system_usage', endpoint=system_usage_endpoint),
        ]
    )


if __name__ == '__main__':
    app = create_app()
    app.run()
