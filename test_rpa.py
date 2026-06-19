import os, sys
sys.path.insert(0, os.path.join(os.getcwd()))
from agent.rpa_executor import execute_rpa
import asyncio
r = asyncio.run(execute_rpa("TEST"))
print("Success:", r.success)
print("Data:", r.extracted_data)
