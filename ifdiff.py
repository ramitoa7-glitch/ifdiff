"""Compare pre/post "show ip interface brief" output, per interface (standard library only)

Usage:
  python ifdiff.py pre.txt post.txt
"""
import sys
from pathlib import Path


def parse_brief(path):
    """Turn "show ip interface brief" into {interface: {ip, status, protocol}}"""
    table = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        parts = line.split()
        # Skip the header, blank lines, prompts, etc. (anything with fewer than 6 columns)
        if len(parts) < 6 or parts[0] == "Interface":
            continue
        name, ip = parts[0], parts[1]
        protocol = parts[-1]
        # Status can be two words ("administratively down"), so join everything in between
        status = " ".join(parts[4:-1])
        table[name] = {"ip": ip, "status": status, "protocol": protocol}
    return table


def compare(pre, post):
    rows = []
    for name in pre.keys() | post.keys():
        if name not in post:
            rows.append((name, "REMOVED", "(missing after the change)"))
        elif name not in pre:
            p = post[name]
            rows.append((name, "ADDED", f"{p['ip']} {p['status']}/{p['protocol']}"))
        else:
            changes = [
                f"{key}: {pre[name][key]} -> {post[name][key]}"
                for key in ("ip", "status", "protocol")
                if pre[name][key] != post[name][key]
            ]
            if changes:
                rows.append((name, "CHANGED", ", ".join(changes)))
    return sorted(rows)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    pre = parse_brief(sys.argv[1])
    post = parse_brief(sys.argv[2])
    rows = compare(pre, post)
    print(f"Before: {len(pre)} / After: {len(post)} / Changes: {len(rows)}")
    for name, kind, detail in rows:
        print(f"[{kind:<7}] {name:<24} {detail}")
    if not rows:
        print("No changes.")


if __name__ == "__main__":
    main()
