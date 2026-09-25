#!/usr/bin/env python3
import json, os, re

BUILD = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(BUILD, ".."))

def main():
    with open(os.path.join(BUILD, "images.json")) as f:
        images = json.load(f)
    with open(os.path.join(BUILD, "template.html"), encoding="utf-8") as f:
        html = f.read()

    missing = []
    for key, b64 in images.items():
        token = "__IMG_%s__" % key
        if token not in html:
            continue
        html = html.replace(token, "data:image/jpeg;base64,%s" % b64)

    leftover = re.findall(r"__IMG_[a-zA-Z0-9]+__", html)
    if leftover:
        missing = sorted(set(leftover))

    out_path = os.path.join(OUT, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    size = os.path.getsize(out_path)
    print(f"wrote {out_path}  ({size/1024:.1f} KB / {size/1024/1024:.3f} MB)")
    if missing:
        print("WARNING: unresolved placeholders:", missing)

if __name__ == "__main__":
    main()
