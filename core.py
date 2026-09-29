"""炼油厂核心逻辑：原油、反应塔、催化剂和压力。"""

import json


def new_game():
    return {
        "batches": {},
        "tower_load": 0,
        "tower_capacity": 100,
        "catalyst": 10,
        "safety": 100,
        "batch_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    return json.loads(text)


def distill(state, batch_id, amount):
    if batch_id in state["batches"]:
        return False
    if state["tower_load"] + amount > state["tower_capacity"]:
        return False
    state["batches"][batch_id] = amount
    state["tower_load"] += amount
    return True


def check_temp(state, temp):
    if temp >= 35:
        return "over"
    return "ok"


def cancel_distill(state, batch_id):
    if batch_id in state["batches"]:
        state["tower_load"] -= state["batches"].pop(batch_id)
    state["catalyst"] = min(10, state["catalyst"] + 2)
    return True


def produce(state, amount):
    if not state.get("catalyst_active", True):
        return False
    return True


def leak(state):
    state["safety"] -= 10
    return state["safety"]


def output(state, amount):
    if state.get("pressure", 1) <= 0:
        return False
    return True


def main():
    print("炼油厂 - 命令: distill/temp/cancel/produce/leak/output/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
