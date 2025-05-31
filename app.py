from flask import Flask, render_template
import psutil
import datetime
import socket

app = Flask(__name__)

@app.route('/')
def index():
    # CPU and Memory
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent

    # Disk
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent

    # Network I/O
    net_io = psutil.net_io_counters()
    bytes_sent = round(net_io.bytes_sent / (1024**2), 2)  # in MB
    bytes_recv = round(net_io.bytes_recv / (1024**2), 2)

    # Uptime
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = str(datetime.datetime.now() - boot_time).split('.')[0]

    # Hostname
    hostname = socket.gethostname()

    # Top 5 Processes
    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']),
                       key=lambda p: p.info['cpu_percent'],
                       reverse=True)[:5]

    return render_template("index.html",
                           cpu_percent=cpu_percent,
                           memory_percent=memory_percent,
                           disk_percent=disk_percent,
                           bytes_sent=bytes_sent,
                           bytes_recv=bytes_recv,
                           uptime=uptime,
                           hostname=hostname,
                           processes=[p.info for p in processes])

if __name__ == "__main__":
    app.run(debug=True)
