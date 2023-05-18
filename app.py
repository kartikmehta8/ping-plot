import subprocess
import re
import time
import matplotlib.pyplot as plt

class PingGraph:
    def __init__(self, ip_address, duration):
        self.ip_address = ip_address
        self.duration = duration
        self.timestamps = []
        self.latencies = []
        self.start_time = time.time()
        self.end_time = self.start_time + duration

    def update_graph(self):
        while time.time() < self.end_time:
            output = subprocess.Popen(['ping', '-c', '1', self.ip_address], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
            latency = re.search(r'time=(\d+.\d+)', output)

            if latency:
                elapsed_time = time.time() - self.start_time
                self.timestamps.append(elapsed_time)
                self.latencies.append(float(latency.group(1)))
                
                plt.clf()
                plt.plot(self.timestamps, self.latencies, marker='o')
                plt.xlabel('Time (s)')
                plt.ylabel('Latency (ms)')
                plt.title('Ping Latency Over Time')
                plt.grid(True)
                plt.ylim(bottom=0, top=max(self.latencies)+10)
                plt.xticks(rotation=45)

                current_latency = self.latencies[-1]
                avg_latency = sum(self.latencies) / len(self.latencies)
                min_latency = min(self.latencies)
                max_latency = max(self.latencies)

                plt.text(0.02, 0.92, f'Current: {current_latency:.2f} ms', transform=plt.gca().transAxes)
                plt.text(0.02, 0.86, f'Average: {avg_latency:.2f} ms', transform=plt.gca().transAxes)
                plt.text(0.02, 0.80, f'Minimum: {min_latency:.2f} ms', transform=plt.gca().transAxes)
                plt.text(0.02, 0.74, f'Maximum: {max_latency:.2f} ms', transform=plt.gca().transAxes)

                plt.pause(0.1)

    def run(self):
        plt.ion()
        self.update_graph()
        plt.ioff()
        plt.show()

ip_address = input('Enter IP address to ping: ')
duration = int(input('Enter duration to ping (in seconds): '))

ping_graph = PingGraph(ip_address, duration)
ping_graph.run()

