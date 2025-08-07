from kubernetes import client, config, watch
from handlers.pod_handler import handle_pod_event

def watch_pods():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    w = watch.Watch()

    print("🚀 Pod 이벤트 감지 시작")

    while True:
        try:
            for event in w.stream(v1.list_pod_for_all_namespaces, timeout_seconds=60):
                event_type = event['type']  # ADDED / MODIFIED / DELETED
                pod = event['object']
                handle_pod_event(event_type, pod)
        except Exception as e:
            print(f"❌ Pod watch 오류: {e}, 재시도 중...")