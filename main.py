import base64
import ast
import os.path
import sys


def read_cdn_ip():
    if not os.path.exists("ip.txt") or os.stat("ip.txt").st_size == 0:
        sys.exit()
    with open('ip.txt', mode='r', encoding='utf-8') as f:
        ips = [ip.strip() for ip in f.readlines()]
        return ips


def update_vmess_node(vmess_base64, remarks=None, address=None, port=None):
    transport_protocol = "vmess://"
    base64_str = vmess_base64.replace(transport_protocol, '', 1)
    decoded = base64.urlsafe_b64decode(base64_str)
    decoded_utf8_str = decoded.decode('utf-8')
    dict_object = ast.literal_eval(decoded_utf8_str)
    if remarks is not None and remarks != '':
        dict_object["ps"] = remarks
    if address is not None and address != '':
        dict_object["add"] = address
    if port is not None and port != '':
        dict_object["port"] = port
    # 编码
    encoded = base64.urlsafe_b64encode(str(dict_object).encode('utf-8'))
    encoded_str = str(encoded, encoding='utf-8')
    new_vmess = transport_protocol + encoded_str
    return new_vmess


if __name__ == '__main__':
    transport_protocol = "vmess://"
    ips = read_cdn_ip()
    print('本程序：将以vmess://开头的节点链接套上优选的CDN，达到提升vmess节点速度的目的。')
    vmess = input("将vmess的节点黏贴到这里(只输入一个节点，不要黏贴一大片)").strip()
    if not vmess.startswith(transport_protocol):
        sys.exit()
    remarks_prefix = input('输入用于区分不同节点的名称/别名的前缀：').strip()
    if remarks_prefix:
        remarks_prefix = f"{remarks_prefix}_"
    with open('output.txt', mode='w', encoding='utf8') as wf:
        for ip in ips:
            new_vmess = update_vmess_node(vmess, remarks=f'{remarks_prefix}{ip}', address=ip)
            wf.write(f"{new_vmess}\n")
    print('成功写入output.txt文件中。')
    print('经过本人测试，生成的节点，可以黏贴到v2rayN中，不能黏贴到NekoBox软件中(需要的，使用其他软件中转，再导入NekoBox软件中)。')
    os.system("pause")