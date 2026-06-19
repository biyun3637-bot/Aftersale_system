"""回复生成节点。基于模板生成客户回复。"""
from models.intent import IntentResult
from agent.decision import Decision


TEMPLATES = {
    "auto_full_refund": """Hi {name},

We checked your order {order_id}. It seems your package has not been delivered.

We have processed a full refund of ${amount} to your original payment method. You should see it within 3-5 business days.

We apologize for the inconvenience.

Best regards,
Customer Service Team""",

    "auto_partial_refund": """Hi {name},

We reviewed your order {order_id} and we understand the issue.

We have issued a partial refund of ${amount} as compensation. The refund will be sent to your original payment method within 3-5 business days.

We appreciate your patience.

Best regards,
Customer Service Team""",

    "human_review": """Hi {name},

Thank you for reaching out about order {order_id}.

Your case has been escalated to our specialized team for review. We will get back to you within 24-48 hours with a resolution.

We appreciate your understanding.

Best regards,
Customer Service Team""",

    "no_action": """Hi {name},

Thank you for contacting us about order {order_id}.

We are looking into this matter and will get back to you shortly.

Best regards,
Customer Service Team""",
}

REVIEW_TEMPLATES = {
    "approve": """Hi {name},

Good news! After reviewing your case for order {order_id}, we have approved your refund of ${amount}.

The refund has been processed to your original payment method. You should see it within 3-5 business days.

We apologize for the inconvenience.

Best regards,
Customer Service Team""",

    "reject": """Hi {name},

Thank you for your patience regarding order {order_id}.

After careful review, we were unable to approve your refund request at this time. Our team has verified the delivery details and found that the order was delivered successfully.

If you have any further questions, please don't hesitate to contact us.

Best regards,
Customer Service Team""",
}


def generate_response(name: str, order_id: str, amount: float, decision_action: str) -> str:
    template = TEMPLATES.get(decision_action, TEMPLATES["no_action"])
    return template.format(name=name, order_id=order_id, amount=f"{amount:.2f}")


def generate_review_response(action: str, name: str, order_id: str, amount: float = 0) -> str:
    template = REVIEW_TEMPLATES.get(action, REVIEW_TEMPLATES["reject"])
    return template.format(name=name, order_id=order_id, amount=f"{amount:.2f}")
