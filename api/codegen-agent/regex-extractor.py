# Copyright contributors to the Qiskit Studio project
# SPDX-License-Identifier: Apache-2.0

import re

try:
    pattern = re.compile(r"```python\s*\n([\s\S]*?)\n```")
    matches = pattern.findall(input[0])
    filtered_matches = [match for match in matches if match]
    result = "\n".join(filtered_matches)
except re.error as e:
    result = f"Invalid regex pattern: {e!s}"
except ValueError as e:
    result = f"Error extracting matches: {e!s}"

output = result
