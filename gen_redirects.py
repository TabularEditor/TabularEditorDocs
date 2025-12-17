#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import posixpath
import sys
import traceback

def main(args: list[str]) -> int:
	config_input_path = "docfx-template.json"
	config_output_path = "docfx.json"
	redirects_path = "redirects.json"
	
	with open(config_input_path) as f:
		config = json.load(f)
	
	with open(redirects_path) as f:
		data : dict[str, str] = json.load(f)
	
	dirs = dict[str, list[str]]()
	for key, value in data.items():
		dir = posixpath.dirname(key)
		if dir in dirs:
			dirs[dir].append(key)
		else:
			dirs[dir] = [key]
		content: list[Any] = config["build"]["content"]
		content.append({"files": posixpath.relpath(key, "content"), "src": "content"})
		os.makedirs(dir, exist_ok=True)
		with open(key, mode="w", encoding="utf-8") as f:
			f.write(f"""---
redirect_url: {value}
---
""")
	
	for dir, files in dirs.items():
		with open(posixpath.join(dir, ".gitignore"), "w") as f:
			f.writelines("/" + posixpath.basename(file) + "\n" for file in files)
			f.write("/.gitignore\n")
	
	with open(config_output_path, "w") as f:
		json.dump(config, f, indent=4)
	
	return 0


if __name__ == "__main__":
	import sys
	try:
		sys.exit(main(sys.argv[1:]))
	except Exception as ex:
		traceback.print_exception(ex, file=sys.stderr)
		sys.exit(1)
