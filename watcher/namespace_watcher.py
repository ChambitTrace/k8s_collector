from kubernetes import client, config, watch
from handlers.namespace_handler import handle_namespace_event

def watch_namespaces():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    w = watch.Watch()

    print("🚀 Namespace 이벤트 감지 시작")

    while True:
        try:
            for event in w.stream(v1.list_namespace, timeout_seconds=60):
                event_type = event['type']
                namespace = event['object']
                handle_namespace_event(event_type, namespace)
        except Exception as e:
            print(f"❌ Namespace watch 오류: {e}, 재시도 중...")
