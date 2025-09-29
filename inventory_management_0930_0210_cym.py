# 代码生成时间: 2025-09-30 02:10:25
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from typing import List, Dict, Any
import uuid

# 模拟数据库存储
class InventoryDatabase:
    def __init__(self):
        self.items = {}

    def add_item(self, item: Dict[str, Any]) -> None:
        self.items[item['id']] = item

    def get_item(self, item_id: str) -> Dict[str, Any]:
        return self.items.get(item_id, None)

    def update_item(self, item_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        if item_id in self.items:
            self.items[item_id].update(updates)
            return self.items[item_id]
        return None

    def delete_item(self, item_id: str) -> bool:
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False

# 库存管理服务
class InventoryService:
    def __init__(self, database: InventoryDatabase):
        self.database = database

    def create_item(self, item: Dict[str, Any]) -> JSONResponse:
        item_id = str(uuid.uuid4())
        self.database.add_item({'id': item_id, **item})
        return JSONResponse({'id': item_id, **item}, status_code=201)

    def read_item(self, item_id: str) -> JSONResponse:
        item = self.database.get_item(item_id)
        if item:
            return JSONResponse(item)
        return JSONResponse({'error': 'Item not found'}, status_code=404)

    def update_item(self, item_id: str, updates: Dict[str, Any]) -> JSONResponse:
        item = self.database.update_item(item_id, updates)
        if item:
            return JSONResponse(item)
        return JSONResponse({'error': 'Item not found'}, status_code=404)

    def delete_item(self, item_id: str) -> JSONResponse:
        if self.database.delete_item(item_id):
            return JSONResponse({'message': 'Item deleted successfully'}, status_code=200)
        return JSONResponse({'error': 'Item not found'}, status_code=404)

# 创建库存管理应用
def create_inventory_app() -> Starlette:
    database = InventoryDatabase()
    service = InventoryService(database)

    app = Starlette(debug=True)

    # 定义路由
    app.add_route('POST', '/items/', lambda request: service.create_item(request.json()))
    app.add_route('GET', '/items/{item_id}', lambda request: service.read_item(request.path_params['item_id']))
    app.add_route('PUT', '/items/{item_id}', lambda request: service.update_item(request.path_params['item_id'], request.json()))
    app.add_route('DELETE', '/items/{item_id}', lambda request: service.delete_item(request.path_params['item_id']))

    return app

# 运行应用
if __name__ == '__main__':
    app = create_inventory_app()
    app.run(host='0.0.0.0', port=8000)
