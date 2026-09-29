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
    state = json.loads(text)
    state["batch_id"] += 1
    return state


def distill(state, batch_id, amount):
    state["batches"][batch_id] = amount
    state["tower_load"] += amount
    return True


def check_temp(state, temp):
    if temp < 30:
        return "over"
    return "ok"


def cancel_distill(state, batch_id):
    return True


def produce(state, amount):
    return True


def leak(state):
    state["safety"] -= 10
    state["safety"] -= 10
    return state["safety"]


def output(state, amount):
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
