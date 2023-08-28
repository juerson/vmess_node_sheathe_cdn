import base64
import ast
import pyperclip  # 将指定的运行结果自动复制到剪切板


# 复制到剪切板中
def copy_to_clipboard(list):
    """
    传入一个列表，将列表转换为字符串，要求：每个元素占据一行
    return : 返回一个由列表中的元素构成的字符串，而且该字符串已经黏贴到剪切板了
    """
    # 使用 `\n` 将每个元素分隔为一个新行
    character_string = "\n".join([item.strip() for item in list])
    # 将字符串复制到剪贴板
    pyperclip.copy(character_string)
    # 返回剪贴板中的内容
    return pyperclip.paste()


# “v2.txt“为存放vmess节点的文件（以vmess://开头的节点）
with open('v2.txt', mode='r', encoding='utf-8') as f:
    prefix_str = input('输入vmess节点的名称或别名的前缀：').strip()
    vmess_hub = []
    for line in f:
        transport_protocol = "vmess://"
        if line.strip() == "" or not line.strip().startswith(transport_protocol):
            continue
        base64_node = line.strip()
        base64_node_new = base64_node.replace(transport_protocol, '')
        # 解码
        decoded_str = base64.urlsafe_b64decode(base64_node_new).decode('utf-8')
        dict_object = ast.literal_eval(decoded_str)
        prefix = f'{prefix_str}_' if prefix_str != '' else ''
        dict_object['ps'] = f"{prefix}{dict_object['add']}:{dict_object['port']}"
        print(dict_object)
        # 编码
        encoded = base64.urlsafe_b64encode(str(dict_object).encode('utf-8'))
        encoded_str = str(encoded, encoding='utf-8')
        new_vmess = transport_protocol + encoded_str
        vmess_hub.append(new_vmess)
    results = copy_to_clipboard(vmess_hub)
    print("已经将结果复制到剪切板，可以黏贴到其他地方。")
