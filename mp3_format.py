from pydub import AudioSegment

"""
音频文件格式转换工具
"""
import os
from pydub import AudioSegment
from pathlib import Path

import utility



def setup_ffmpeg():
    """设置 ffmpeg 路径"""
    try:
        # 设置 ffmpeg 路径
        ffmpeg_path = r"D:\Tools\ffmpeg6\bin"  # 请确保这是你的 ffmpeg 安装路径
        if os.path.exists(ffmpeg_path):
            os.environ["PATH"] += os.pathsep + ffmpeg_path
        else:
            print("警告: 未找到 ffmpeg，请安装 ffmpeg 并设置正确的路径")
            print("下载地址: https://www.gyan.dev/ffmpeg/builds/")
            print("1. 下载 ffmpeg")
            print("2. 解压到 C:\\ffmpeg")
            print("3. 将 C:\\ffmpeg\\bin 添加到系统环境变量")
            return False
        return True
    except Exception as e:
        print(f"设置 ffmpeg 失败: {e}")
        return False

def convert_sing(src_file, dst_file):
    try:
        # 检查源文件是否存在
        if not os.path.exists(src_file):
            print(f"{src_file} -> 源文件不存在，跳过")
            return False

        # 如果mp3文件已存在，跳过转换
        if os.path.exists(dst_file):
            print(f"{dst_file} -> 已存在，跳过")
            return True

        print(f"正在转换 {src_file}...")

        # 使用 ffmpeg 直接转换
        cmd = f'ffmpeg -i "{src_file}" -acodec libmp3lame -ab 320k "{dst_file}"'
        result = os.system(cmd)

        if result == 0:
            print(f"[{src_file} -> 转换成功")
        else:
            print(f"{src_file} -> 转换失败")

        os.remove(dst_file)
    except Exception as e:
        print(f"{src_file} -> 转换失败: {e}")
def convert_m4a_to_mp3(input_folder: str, output_folder: str):
    """
    将文件夹中的所有m4a文件转换为mp3

    Args:
        input_folder: 输入文件夹路径
        output_folder: 输出文件夹路径
    """
    try:
        # 确保输出目录存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 获取所有m4a文件
        # m4a_files = list(Path(input_folder).glob('*.m4a'))
        m4a_files = list(Path(input_folder).glob('*.aac'))
        total = len(m4a_files)

        print(f"找到 {total} 文件")

        # 转换每个文件
        for i, src_file in enumerate(m4a_files, 1):
            try:
                # 检查源文件是否存在
                if not os.path.exists(src_file):
                    print(f"[{i}/{total}] {src_file.name} -> 源文件不存在，跳过")
                    continue

                # 构建输出文件路径
                dst_file_name = os.path.join(output_folder, f"{src_file.stem}.mp3")

                # 如果mp3文件已存在，跳过转换
                if os.path.exists(dst_file_name):
                    print(f"[{i}/{total}] {src_file.name} -> 已存在，跳过")
                    continue

                print(f"[{i}/{total}] 正在转换 {src_file.name}...")

                # 使用 ffmpeg 直接转换
                cmd = f'ffmpeg -i "{src_file}" -acodec libmp3lame -ab 320k "{dst_file_name}"'
                result = os.system(cmd)

                if result == 0:
                    print(f"[{i}/{total}] {src_file.name} -> 转换成功")
                else:
                    print(f"[{i}/{total}] {src_file.name} -> 转换失败")

                os.remove(dst_file_name)
            except Exception as e:
                print(f"[{i}/{total}] {src_file.name} -> 转换失败: {e}")
                continue

        print("\n转换完成!")
        print(f"输出目录: {output_folder}")

    except Exception as e:
        print(f"转换过程出错: {e}")

def list_files_in_directory(root_dir):
    aac_suffix = ".aac"
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            src_file = os.path.join(root, file)
            file_path = Path(src_file)
            suffix = file_path.suffix
            stem = file_path.stem
            if aac_suffix.casefold() == suffix.casefold():
                dst_file = root + "\\" + stem + ".mp3"
                convert_sing(src_file, dst_file)
                # print(f"root:{root}, srcfile:{src_file}, dstfile:{dst_file}")  # 打印文件完整路径


if __name__ == "__main__":
    # 检查 ffmpeg
    if not setup_ffmpeg():
        print("setup ffmpeg failed")

    # 设置输入和输出文件夹
    input_folder = "D:\\tmp123\\MP3"
    output_folder = "D:\\tmp123\\MP3"

    src_path = "D:\\work\\stella\\play_short_20250404_finish\\dstPath"
    list_files_in_directory(src_path)


    # 开始转换
    # convert_m4a_to_mp3(input_folder, output_folder)
