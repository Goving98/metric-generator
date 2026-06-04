import threading
import time
import random
import uvicorn

from core.load_engine import LoadEngine
from payment_service.simulator import PaymentService
from order_service.simulator import OrderService
from api.server import app

payment = PaymentService()
order = OrderService(payment)
engine = LoadEngine(max_workers=120)

current_rps = 20
system_mode = "NORMAL"


def update_mode():
    global system_mode

    roll = random.random()

    if roll < 0.7:
        system_mode = "NORMAL"
    elif roll < 0.85:
        system_mode = "SPIKE"
    elif roll < 0.95:
        system_mode = "DEGRADED"
    else:
        system_mode = "OUTAGE"

    payment.set_mode(system_mode)
    order.set_mode(system_mode)


def update_rps():
    global current_rps

    if system_mode == "NORMAL":
        target = random.randint(20, 40)
    elif system_mode == "SPIKE":
        target = random.randint(80, 120)
    elif system_mode == "DEGRADED":
        target = random.randint(40, 70)
    else:
        target = random.randint(10, 30)

    current_rps += (target - current_rps) * 0.3
    return int(current_rps)


def simulation_loop():
    tick = 0

    while True:
        if tick % 10 == 0:
            update_mode()

        rps = update_rps()
        engine.generate_load(rps, order.process)

        time.sleep(1)
        tick += 1


if __name__ == "__main__":
    threading.Thread(target=simulation_loop, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)