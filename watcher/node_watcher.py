from kubernetes import client, config, watch
from handlers.node_handler import handle_node_event

def watch_nodes():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    w = watch.Watch()

    print("🚀 Node 이벤트 감지 시작")

    while True:
        try:
            for event in w.stream(v1.list_node, timeout_seconds=60):
                event_type = event['type']
                node = event['object']
                handle_node_event(event_type, node)
        except Exception as e:
            print(f"❌ Node watch 오류: {e}, 재시도 중...")