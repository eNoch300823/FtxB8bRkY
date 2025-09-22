# 代码生成时间: 2025-09-22 14:01:10
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
import uvicorn

# 模拟数据库
inventory_db = {
    "items": [
        {
            "item_id": 1,
            "name": "Item A",
            "quantity": 10
        },
        {
            "item_id": 2,
            "name": "Item B",
            "quantity": 20
        }
    ]
}

# 获取所有库存项
async def get_all_inventory(request):
    """
    Endpoint to retrieve all inventory items.
    """
    return JSONResponse(inventory_db, status_code=HTTP_200_OK)

# 获取单个库存项
async def get_inventory_item(request):
    """
    Endpoint to retrieve a single inventory item by item_id.
    """
    item_id = request.path_params.get('item_id')
    if item_id is None:
        return JSONResponse(
            {'detail': 'Item ID is required'}, status_code=HTTP_400_BAD_REQUEST
        )
    
    item_id = int(item_id)
    for item in inventory_db['items']:
        if item['item_id'] == item_id:
            return JSONResponse(item, status_code=HTTP_200_OK)
    
    return JSONResponse(
        {'detail': 'Item not found'}, status_code=HTTP_404_NOT_FOUND
    )

# 更新库存项数量
async def update_inventory_item(request):
    """
    Endpoint to update the quantity of an inventory item by item_id.
    """
    item_id = request.path_params.get('item_id')
    if item_id is None or not request.json or 'quantity' not in request.json:
        return JSONResponse(
            {'detail': 'Item ID and quantity are required'}, status_code=HTTP_400_BAD_REQUEST
        )
    
    item_id = int(item_id)
    item_quantity = request.json['quantity']
    
    for item in inventory_db['items']:
        if item['item_id'] == item_id:
            item['quantity'] = item_quantity
            return JSONResponse(item, status_code=HTTP_200_OK)
    
    return JSONResponse(
        {'detail': 'Item not found'}, status_code=HTTP_404_NOT_FOUND
    )

# 路由列表
routes = [
    Route('/inventory', get_all_inventory, methods=['GET']),
    Route('/inventory/{item_id:int}', get_inventory_item, methods=['GET']),
    Route('/inventory/{item_id:int}', update_inventory_item, methods=['PATCH'])
]

# 创建Starlette应用
app = Starlette(debug=True, routes=routes)

# 运行服务器
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)