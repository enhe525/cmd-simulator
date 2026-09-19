# CMD Simulator

用 Python 实现的 Windows CMD 命令行模拟器。

## 功能

- 模拟 Windows CMD 启动界面
- 支持 `dir` 命令（复刻原生排版）
- 支持 `cd`、`echo`、`cls`、`history` 等常用命令
- 命令历史记录与 `!数字` 快速执行
- 环境变量替换
- 外部命令执行

## 文件说明

- `main.py` - 主程序源码
- `dist/main.exe` - 打包后的可执行文件

## 使用方法

直接运行 `main.py` 或 `dist/main.exe` 即可启动模拟器。

## 开发说明

打包命令：
```
pyinstaller --onefile main.py
```
