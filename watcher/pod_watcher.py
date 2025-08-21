from kubernetes import client, config, watch
from handlers.pod_handler import handle_pod_event, init_pod_sync

def watch_pods():
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()

    v1 = client.CoreV1Api()
    w = watch.Watch()

    print("🚀 Pod 이벤트 감지 시작")
    init_pod_sync()
    while True:
        try:
            for event in w.stream(v1.list_pod_for_all_namespaces, timeout_seconds=60):
                event_type = event['type']  # ADDED / MODIFIED / DELETED
                pod = event['object']
                print(f"🐛 Debug: Pod '{pod.metadata.name}' 이벤트 타입: {event_type}")
                handle_pod_event(event_type, pod)
        except Exception as e:
            print(f"❌ Pod watch 오류: {e}, 재시도 중...")