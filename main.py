from watcher.pod_watcher import watch_pods
from watcher.node_watcher import watch_nodes
from watcher.namespace_watcher import watch_namespaces
from db.database import check_db_connection

import threading

if __name__ == "__main__":
    print("🔥 Collector 시작됨")
    if check_db_connection():
        threading.Thread(target=watch_pods).start()
        threading.Thread(target=watch_nodes).start()
        threading.Thread(target=watch_namespaces).start()
    else:
        print("❌ Collector를 시작할 수 없습니다. 데이터베이스 연결을 확인하세요.")
