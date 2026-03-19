from kubernetes import client, config

def get_namespace_events(namespace):
    try:
        config.load_kube_config(context="docker-desktop")
    except:
        config.load_kube_config()

    v1 = client.CoreV1Api()
    events = v1.list_namespaced_event(namespace, limit=2)

    event_list = []

    for e in events.items[-10:]:
        event_list.append(
            f"{e.type} | {e.reason} | {e.message}"
        )

    if not event_list:
        return "No recent events found"

    return "\n".join(event_list)
