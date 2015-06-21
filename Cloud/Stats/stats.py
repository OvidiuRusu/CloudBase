import psutil
import platform
import socket


class PerformanceStats(object):

    """docstring for PerformanceStats"""

    def __init__(self):
        super(PerformanceStats, self).__init__()

    def getStats(self):
        result = {}
        ip = str(socket.gethostbyname(socket.gethostname()))
        user = platform.node()
        try:
            pids = psutil.pids()
            for pid in pids:
                p = psutil.Process(pid)
                try:
                    if pid in (0, 4) or not p.name():
                        continue
                    result[pid] = {'PC': user, 'IP': ip, 'name': p.name(), 'CPU': float(p.cpu_percent(interval=0.1)), 'Memory': float((p.memory_info_ex().private / 1048576)), 'ReadB/s': p.io_counters().read_bytes, 'WriteB/s': p.io_counters().write_bytes, 'Threads': p.num_threads(
                    )}
                except psutil.AccessDenied:
                    pass
        except psutil.NoSuchProcess:
            pass
        result['total'] = {'CPU_Percent': psutil.cpu_percent(interval=1), 'Virtual_Memory': psutil.virtual_memory().percent, 'Disk_Usage': psutil.disk_usage('/').percent}
        return result


if __name__ == '__main__':

    perf = PerformanceStats()
    print perf.getStats()
