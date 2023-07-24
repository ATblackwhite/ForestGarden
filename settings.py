SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
# 设置刷新率
FPS = 60

# 设置渲染顺序
LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10
    }
PLANT_ATTRIBUTE = {
    'fruittree': (0.02, 1000, 20),  # (grow_speed, life, stages)
    'greentree': (0.02, 1000, 20),   # (grow_speed, life, stages)
}
# 设置瓦片大小
TILE_SIZE = 64