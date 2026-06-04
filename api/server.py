from fastapi import FastAPI
from payment_service.simulator import PaymentService
from order_service.simulator import OrderService

app = FastAPI()

payment = PaymentService()
order = OrderService(payment)


@app.get("/metrics")
def get_metrics():
    return {
        "payment": payment.metrics(),
        "order": order.metrics()
    }


@app.get("/health")
def health():
    return {"status": "ok"}