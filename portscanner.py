#!/usr/bin/python3

from argparse import ArgumentParser
import socket
from threading import Thread, Lock
from time import time

open_ports = []
lock = Lock()

def prepare_args():
    """Prepare arguments
    
    Returns:
        args (argparse.Namespace): Parsed arguments
    """
    parser = ArgumentParser(description="Python Based Port Scanner", 
                            usage="%(prog)s 0.0.0.0", 
                            epilog="Example - %(prog)s -s 20 -e 40000 -t 500 -V 0.0.0.0")
    parser.add_argument(metavar="IPv4", dest="IP", help="host to scan")
    parser.add_argument("-s", "--start", dest="start", metavar="", type=int, help="starting port", default=1)
    parser.add_argument("-e", "--end", dest="end", metavar="", type=int, help="ending port", default=65535)
    parser.add_argument("-t", "--threads", dest="threads", metavar="", type=int, help="threads to use", default=500)
    parser.add_argument("-V", "--verbose", dest="verbose", action="store_true", help="verbose output")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    args = parser.parse_args()
    return args

def prepare_ports(start: int, end: int):
    """Generator function for ports
    
    Arguments:
        start (int): Starting port
        end (int): Ending port
    
    Yields:
        int: Port number
    """
    for port in range(start, end + 1):
        yield port

def scan_port():
    """Scan ports"""
    while True:
        try:
            sckt = socket.socket()
            sckt.settimeout(1)
            port = next(ports)
            sckt.connect((arguments.IP, port))
            with lock:
                open_ports.append(port)
            if arguments.verbose:
                print(f"\r{open_ports}", end="")
        except (ConnectionRefusedError, socket.timeout):
            continue
        except StopIteration:
            break

def prepare_threads(threads: int):
    """Create, start & join threads
    
    Arguments:
        threads (int): Number of threads to use
    """
    thread_list = []
    for i in range(threads):
        thread = Thread(target=scan_port)
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    arguments = prepare_args()
    ports = prepare_ports(arguments.start, arguments.end)
    start_time = time()
    prepare_threads(arguments.threads)
    end_time = time()
    if arguments.verbose:
        print()
    print(f"Open Ports Found: {open_ports}")
    print(f"Time taken to scan: {round(end_time - start_time, 2)} seconds")
