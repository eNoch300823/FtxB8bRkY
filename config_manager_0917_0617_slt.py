# 代码生成时间: 2025-09-17 06:17:17
import starlette.config as config

# 配置文件管理器
class ConfigManager:
    def __init__(self):
        """
        初始化配置文件管理器
        """
        self.config = config.Config(".env")

    def get(self, key):
        """
        从配置文件中获取指定键的值
        
        :param key: 键名
        :return: 键对应的值
        """
        try:
            return self.config(key)
        except KeyError:
            # 如果配置文件中没有对应的键，则抛出异常
            raise KeyError(f"Config key '{key}' not found")

    def set(self, key, value):
        """
        将指定键的值设置到配置文件中
        
        :param key: 键名
        :param value: 键对应的值
        """
        try:
            # 将值写入配置文件
            with open(self.config.config_file_path, 'a') as f:
                f.write(f"
{key}={value}")
        except Exception as e:
            # 处理写入配置文件时可能出现的错误
            raise Exception(f"Failed to write to config file: {str(e)}")

    def delete(self, key):
        """
        从配置文件中删除指定键
        
        :param key: 键名
        """
        try:
            # 读取配置文件内容
            with open(self.config.config_file_path, 'r') as f:
                lines = f.readlines()
            
            # 过滤掉要删除的键对应的行
            with open(self.config.config_file_path, 'w') as f:
                for line in lines:
                    if line.strip() != f"{key}=":
                        f.write(line)
        except Exception as e:
            # 处理读取或写入配置文件时可能出现的错误
            raise Exception(f"Failed to delete config key: {str(e)}")

# 示例
if __name__ == '__main__':
    config_manager = ConfigManager()
    
    # 获取配置项
    print(config_manager.get('DATABASE_URL'))
    
    # 设置配置项
    config_manager.set('API_KEY', 'your_api_key_here')
    
    # 删除配置项
    config_manager.delete('API_KEY')