import argparse
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import re
import socket
import struct
from ping3 import ping
import time
import json


def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


def parse_ip_range(ip_range):
    matches = re.match(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\-"
                       r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", ip_range)
    if matches is None:
        raise ValueError('bad format of ip range')

    ips = matches.groups()
    ip_int32_from = ip2int(ips[0])
    ip_int32_to = ip2int(ips[1])
    if ip_int32_from > ip_int32_to:
        raise ValueError('bad ip range')

    return ip_int32_from, ip_int32_to


def is_port_open(ip: str, port: int) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    loc = (ip, port)
    result = s.connect_ex(loc)
    s.close()
    return result == 0

def ping_host(ip):
    result = ping(ip, timeout=1)
    return type(result) == float and result > 0.0


def create_task_generator(task_type, ip_from, ip_to):
    if task_type == 'tcp':
        for int32_ip in range(ip_from, ip_to + 1):
            str_ip = int2ip(int32_ip)
            for port in range(1, 65535 + 1):
                yield is_port_open, str_ip, port
    else:
        for int32_ip in range(ip_from, ip_to + 1):
            yield ping_host, int2ip(int32_ip)


def measure_time(func, *args):
    start_time = time.time()
    ret = func(*args)
    elapsed = time.time() - start_time
    return ret, elapsed


def save_json(filename, file):
    with open(filename, 'w') as file_obj:
        json.dump(file, file_obj)


def current_run(is_proc, num_of_workers, task_generator, enable_measurement, enable_save):
    file_name = 'result.json'
    result = []
    klass = globals()['ThreadPoolExecutor']
    if is_proc:
        klass = globals()['ProcessPoolExecutor']

    with klass(max_workers=num_of_workers) as executor:
        futures = {}
        for t in task_generator:
            func = t[0]
            args = list(t)
            args.pop(0)
            if enable_measurement:
                future = executor.submit(measure_time, func, *args)
            else:
                future = executor.submit(func, *args)
            futures[future] = t

        for f in concurrent.futures.as_completed(futures):
            tt = futures[f]
            ip = tt[1]
            port = 0
            if len(tt) == 3:
                port = tt[2]
            r = f.result()
            if enable_measurement:
                print(ip, port, r[0], r[1])
                result.append((ip, port, r[0], r[1]))
            else:
                print(ip, port, r)
                result.append((ip, port, r))
    if enable_save:
        save_json(file_name, result)

def main():
    """
    -n：指定并发数量。
    -f ping：进行 ping 测试
    -f tcp：进行 tcp 端口开放、关闭测试。
    -ip：连续 IP 地址支持 192.168.0.1-192.168.0.100 写法。
    -w：扫描结果进行保存。
    通过参数 [-m proc|thread] 指定扫描器使用多进程或多线程模型。
    增加 -v 参数打印扫描器运行耗时 (用于优化代码)。
    扫描结果显示在终端，并使用 json 格式保存至文件。
    :return:
    """
    parser = argparse.ArgumentParser(description='scanner')
    parser.add_argument('-n', type=int, default=12, help='number of concurrent')
    parser.add_argument('-f', choices=['ping', 'tcp'], default='tcp', help='ping or tcp protocol')
    parser.add_argument('-ip', type=str, required=True, help='ip range 192.168.0.1-192.168.0.100')
    parser.add_argument('-w', action='count', default=0, help='save to file')
    parser.add_argument('-m', choices=['proc', 'thread'], default='proc', help='multiprocess or multithread',
                        required=False)
    parser.add_argument('-v', action='count', default=0, help='show elapsed time')
    args = parser.parse_args()

    # print(ip_range)

    ip_range = parse_ip_range(args.ip)
    task_gen = create_task_generator(args.f, ip_range[0], ip_range[1])
    current_run(args.m == 'proc', args.n, task_gen, args.v > 0, args.w > 0)


if __name__ == '__main__':
    main()
