import os
root = os.path.join(os.getcwd())
code = r"""
import os as _o
def _mp():
    b = _o.path.dirname(_o.path.abspath(__file__))
    return _o.path.abspath(_o.path.join(b, "..", "rpa", "mock_pages", "shopify_order.html"))
def test():
    print("MOCK PAGE:", _mp())
test()
"""
with open(os.path.join(root, 'agent', 'rpa_executor.py'), 'w', encoding='utf-8') as f:
    f.write(code)
print("Written")
