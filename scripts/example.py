#!/usr/bin/env python3

import json
from cli import results

print(json.dumps(results, indent=4, default=lambda obj: str(obj)))
