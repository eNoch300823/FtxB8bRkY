# 代码生成时间: 2025-09-22 14:54:45
import os
import shutil
import logging
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request

# 配置日志
logging.basicConfig(level=logging.INFO)

class FileBackupSyncApp(Starlette):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.routes = [
            Route("/backup", self.backup_files),
            Route("/sync", self.sync_files),
        ]

    async def backup_files(self, request: Request):
        """
        备份文件的接口
        :param request: 请求对象
        :return: JSONResponse
        """
        try:
            source_path = request.query_params.get("source")
            target_path = request.query_params.get("target\)
            if not source_path or not target_path:
                return JSONResponse(
                    content={"message": "Missing source or target path"},
                    status_code=400,
                )
            # 确保源路径存在
            if not os.path.exists(source_path):
                return JSONResponse(
                    content={"message": f"Source path {source_path} does not exist"},
                    status_code=404,
                )
            # 执行文件备份
            shutil.copytree(source_path, target_path)
            return JSONResponse(content={"message": "Backup successful"})
        except Exception as e:
            logging.error(f"Error during backup: {e}")
            return JSONResponse(
                content={"message": f"An error occurred: {e}"},
                status_code=500,
            )

    async def sync_files(self, request: Request):
        """
        同步文件的接口
        :param request: 请求对象
        :return: JSONResponse
        """
        try:
            source_path = request.query_params.get("source")
            target_path = request.query_params.get("target")
            if not source_path or not target_path:
                return JSONResponse(
                    content={"message": "Missing source or target path"},
                    status_code=400,
                )
            # 确保源路径和目标路径存在
            if not os.path.exists(source_path) or not os.path.exists(target_path):                return JSONResponse(
                    content={"message": f"Source or target path does not exist"},
                    status_code=404,
                )
            # 执行文件同步
            shutil.copytree(source_path, target_path)
            return JSONResponse(content={"message": "Sync successful"})
        except Exception as e:
            logging.error(f"Error during sync: {e}")
            return JSONResponse(
                content={"message": f"An error occurred: {e}"},
                status_code=500,
            )

# 运行应用程序
if __name__ == "__main__":
    app = FileBackupSyncApp()
    uvicorn.run(app, host="0.0.0.0", port=8000)