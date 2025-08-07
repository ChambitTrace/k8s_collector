# handlers/node_handler.py

def handle_node_event(event_type, node_obj):
    node_name = node_obj.metadata.name
    created_at = node_obj.metadata.creation_timestamp

    zone = node_obj.metadata.labels.get("topology.kubernetes.io/zone") or \
           node_obj.metadata.labels.get("failure-domain.beta.kubernetes.io/zone", "unknown")

    if event_type == 'ADDED':
        print(f"[+] Node 생성: {node_name} (zone={zone})")
        # PostgreSQL INSERT
    elif event_type == 'MODIFIED':
        print(f"[~] Node 변경: {node_name} (zone={zone})")
        # PostgreSQL UPDATE
    elif event_type == 'DELETED':
        print(f"[-] Node 삭제: {node_name}")
        # PostgreSQL DELETE