# handlers/pod_handler.py

def handle_pod_event(event_type, pod_obj):
    pod_name = pod_obj.metadata.name
    namespace = pod_obj.metadata.namespace
    node_name = pod_obj.spec.node_name
    created_at = pod_obj.metadata.creation_timestamp

    if event_type == 'ADDED':
        print(f"[+] Pod 생성: {namespace}/{pod_name}")
        # PostgreSQL INSERT
    elif event_type == 'MODIFIED':
        print(f"[~] Pod 변경: {namespace}/{pod_name}")
        # PostgreSQL UPDATE
    elif event_type == 'DELETED':
        print(f"[-] Pod 삭제: {namespace}/{pod_name}")
        # PostgreSQL DELETE