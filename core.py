"""炼油厂核心逻辑：原油、反应塔、催化剂和压力。"""

import json


def new_game():
    return {
        "batches": {},
        "tower_load": 0,
        "tower_capacity": 100,
        "catalyst": 10,
        "catalyst_active": True,
        "safety": 100,
        "pressure": 1,
        "produced": 0,
        "out_amount": 0,
        "batch_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("empty save data")
    state = json.loads(text)
    if not isinstance(state, dict):
        raise ValueError("invalid save data")
    base = new_game()
    for key, value in base.items():
        state.setdefault(key, value)
    return state


def _positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def distill(state, batch_id, amount):
    if not _positive_number(amount):
        return False
    if batch_id in state["batches"]:
        return False
    if state["tower_load"] + amount > state["tower_capacity"]:
        return False
    state["batches"][batch_id] = amount
    state["tower_load"] += amount
    return True


def check_temp(state, temp):
    if not isinstance(temp, (int, float)) or isinstance(temp, bool):
        return "invalid"
    if temp > 30:
        return "over"
    return "ok"


def cancel_distill(state, batch_id):
    if batch_id in state["batches"]:
        state["tower_load"] -= state["batches"].pop(batch_id)
        if state["tower_load"] < 0:
            state["tower_load"] = 0
    state["catalyst"] = min(10, state["catalyst"] + 2)
    return True


def produce(state, amount):
    if not state.get("catalyst_active", False):
        return False
    if not _positive_number(amount):
        return False
    if state["catalyst"] <= 0:
        return False
    state["produced"] = state.get("produced", 0) + amount
    return True


def leak(state):
    state["safety"] -= 10
    if state["safety"] < 0:
        state["safety"] = 0
    return state["safety"]


def output(state, amount):
    if state.get("pressure", 1) != 1:
        return False
    if not _positive_number(amount):
        return False
    if amount > state["tower_load"]:
        return False
    state["tower_load"] -= amount
    state["out_amount"] = state.get("out_amount", 0) + amount
    return True


def main():
    print("炼油厂 - 命令: distill/temp/cancel/produce/leak/output/quit")
    state = new_game()
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        parts = raw.split()
        command = parts[0]
        args = parts[1:]
        if command == "distill" and len(args) == 2:
            try:
                print(distill(state, int(args[0]), float(args[1])))
            except ValueError:
                print("unknown")
        elif command == "temp" and len(args) == 1:
            try:
                print(check_temp(state, float(args[0])))
            except ValueError:
                print("unknown")
        elif command == "cancel" and len(args) == 1:
            try:
                print(cancel_distill(state, int(args[0])))
            except ValueError:
                print("unknown")
        elif command == "produce" and len(args) == 1:
            try:
                print(produce(state, float(args[0])))
            except ValueError:
                print("unknown")
        elif command == "leak" and not args:
            print(leak(state))
        elif command == "output" and len(args) == 1:
            try:
                print(output(state, float(args[0])))
            except ValueError:
                print("unknown")
        else:
            print("unknown")


if __name__ == "__main__":
    main()
