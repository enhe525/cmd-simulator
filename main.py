import os
import re
import time
import shutil

# ===================== 基础函数（保留你的原版，小幅优化）=====================
def slow_print(s, delay=0.04):
    for c in s:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

slow_print("Microsoft Windows [版本 10.0.19045.6466]")
slow_print("(c) Microsoft Corporation。保留所有权利。")
print()

def quote_all_paths(cmd_text):
    pattern = r'[A-Za-z]:[\\/][^\s]*'
    def wrap_path(match):
        path = match.group(0)
        if " " in path and not (path.startswith('"') and path.endswith('"')):
            return f'"{path}"'
        return path
    return re.sub(pattern, wrap_path, cmd_text)

def replace_env_vars(text):
    pattern = r'%(\w+)%'
    def do_replace(match):
        var_name = match.group(1)
        return os.getenv(var_name, match.group(0))
    return re.sub(pattern, do_replace, text)

history_list = []
max_history = 100
# 解决打包/源码上下键乱码，取消注释安装依赖：pip install pyreadline3
# import pyreadline3

os.system("chcp 65001 > nul")

def show_history():
    """模拟 doskey /history"""
    print("===== 命令历史列表 =====")
    for index, cmd in enumerate(history_list):
        print(f"{index:3d} | {cmd}")
    print("输入 !数字 快速执行对应历史命令")

# =====================【重点重写dir命令，复刻CMD原生排版】=====================
def cmd_dir():
    """实现和截图一致的标准dir输出（Windows兼容版）"""
    current = os.getcwd()
    # 磁盘盘符
    drive = os.path.splitdrive(current)[0]
    print(f" 驱动器 {drive} 中的卷没有标签。")
    vol_serial = "1C78-9FD3"
    print(f" 卷的序列号是 {vol_serial}\n")
    print(f" {current} 的目录\n")

    file_cnt = 0
    dir_cnt = 0
    total_size = 0

    for entry in os.scandir(current):
        mtime = time.localtime(entry.stat().st_mtime)
        date_str = time.strftime("%Y/%m/%d %H:%M", mtime)
        if entry.is_dir(follow_symlinks=False):
            print(f"{date_str}    <DIR>          {entry.name}")
            dir_cnt += 1
        else:
            fsize = entry.stat().st_size
            total_size += fsize
            print(f"{date_str}     {fsize:>14,} {entry.name}")
            file_cnt += 1
    print(f"              {file_cnt:2d} 个文件    {total_size:>14,} 字节")
    # Windows兼容获取磁盘可用空间
    disk_info = shutil.disk_usage(current)
    free_bytes = disk_info.free
    print(f"              {dir_cnt:2d} 个目录  {free_bytes:>14,} 可用字节\n")
# ===================== 主循环 =====================
while True:  
    current_path = os.getcwd()  
    raw_input_cmd = input(f"{current_path} > ")  
    cmd_ori = raw_input_cmd.strip()  
    cmd_low = cmd_ori.lower()  
  
    # 历史记录去重  
    if not history_list or history_list[-1] != raw_input_cmd:  
        history_list.append(raw_input_cmd)  
        if len(history_list) > max_history:  
            history_list.pop(0)  
  
    if cmd_low == "history":  
        show_history()  
        continue  
  
    # !编号执行历史命令  
    if cmd_ori.startswith("!") and cmd_ori[1:].isdigit():  
        target_idx = int(cmd_ori[1:])  
        if 0 <= target_idx < len(history_list):  
            raw_input_cmd = history_list[target_idx]  
            print(f"> 调用历史命令：{raw_input_cmd}")  
        else:
            print("错误：不存在该历史编号")  
            continue  
  
    if cmd_low == "exit":  
        break  
    if cmd_low == "cls":  
        os.system("cls")
        continue  
  
    # 替换原版简陋dir，替换为完整排版版本  
    if cmd_low.startswith("dir"):  
        cmd_dir()  
        continue  
  
    if cmd_low == "ls":  
        print("\n".join(os.listdir(current_path)))
        continue  
  
    # cd 逻辑完全沿用你写的原版  
    if cmd_low.startswith("cd"):  
        cmd_parts = raw_input_cmd.split()  
        if len(cmd_parts) == 1:  
            print(os.getcwd())
            continue  
  
        offset = 1  
        if cmd_parts[1].lower() == "/d":  
            offset = 2  
        target_dir = " ".join(cmd_parts[offset:]).strip('"')  
        target_dir = replace_env_vars(target_dir)  
        try:  
            os.chdir(target_dir)  
        except FileNotFoundError:  
            print("系统找不到指定的路径。")  
        except NotADirectoryError:  
            print("指定的路径不是文件夹哦。")  
        continue  
  
    # ===== 新增：处理 echo 命令 =====  
    if cmd_low.startswith("echo"):  
        # 如果包含 > 或 >>，交给系统处理  
        if ">" in cmd_ori:  
            os.system(cmd_ori)
        else:  
            echo_content = cmd_ori[4:].strip()  
            if not echo_content:  
                print()
            else:  
                echo_content = replace_env_vars(echo_content)  
                print(echo_content)
        continue  
  
    # 外部命令执行（不再替换环境变量，让系统CMD自己处理）  
    exec_cmd = quote_all_paths(raw_input_cmd)
    if ":"not in exec_cmd:
        os.system(exec_cmd)
    if "set" in exec_cmd:
        print()