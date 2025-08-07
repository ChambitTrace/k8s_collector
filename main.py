from watcher.pod_watcher import watch_pods
from watcher.node_watcher import watch_nodes
import threading

if __name__ == "__main__":
    threading.Thread(target=watch_pods).start()
    threading.Thread(target=watch_nodes).start()