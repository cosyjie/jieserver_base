def remove_list_blank(list_object):
    """
    移除列表中的空字符串元素
    Args:
        list_object (list): 需要处理的列表对象

    Returns:
        list: 移除空字符串元素后的列表对象
    """
    return [i for i in list_object if i != '']


def subprocess_run(subprocess, exec_statement):
    """
    执行subprocess.run方法来运行指定的命令，并返回命令的输出结果。

    参数：
    subprocess: subprocess模块的对象
    exec_statement: 要执行的命令字符串

    返回值：
    subprocess.run方法的返回值

    示例：
    >>> subprocess_run(subprocess, "ls -l")
    """
    return subprocess.run(exec_statement, shell=True, capture_output=True, encoding='utf-8')


def read_file(filepath, mode='r'):
    """
    读取文件内容
    @filename 文件名
    return string(bin) 若文件不存在，则返回None
    """
    from pathlib import Path

    if not Path(filepath): return False
    fp = None
    try:
        fp = open(filepath, mode)
        f_content = fp.read()
    except Exception as ex:
        fp = open(filepath, mode, encoding="utf-8", errors='ignore')
        f_content = fp.read()
    finally:
        if fp and not fp.closed: fp.close()
    return f_content


def write_file(filename, content, mode='w+'):
    """
    写入文件内容
    @filename 文件名
    @s_body 欲写入的内容
    return bool 若文件不存在则尝试自动创建
    """
    try:
        fp = open(filename, mode)
        fp.write(content)
        fp.close()
        return True
    except:
        try:
            fp = open(filename, mode, encoding="utf-8")
            fp.write(content)
            fp.close()
            return True
        except:
            return False


def make_dir(dir_path):
    """ 判断是否存在目录，如果不存在就创建 """
    try:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
    except:
        return False
