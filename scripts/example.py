#!/usr/bin/env python3

import json
from cli import result

print(json.dumps(result, indent=4, default=lambda obj: str(obj)))
