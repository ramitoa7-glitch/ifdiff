# ifdiff

Compare `show ip interface brief` output **before and after a network change**, per interface.

A single Python file. Standard library only. No device connection — it just reads text files you have already saved.

```text
$ python ifdiff.py examples/pre.txt examples/post.txt
Before: 6 / After: 7 / Changes: 3
[CHANGED] GigabitEthernet1/0/2     status: up -> down, protocol: up -> down
[CHANGED] GigabitEthernet1/0/4     status: administratively down -> up, protocol: down -> up
[ADDED  ] Vlan30                   203.0.113.1 up/up
```

## Why not just `diff`?

A line diff shows *that* something changed. You still have to read the columns to see *which interface, which field, and how*. Prompt lines and reordered lines add noise.

`ifdiff` parses each output into a table keyed by interface name, then reports:

- **ADDED** — interfaces that only exist after the change
- **REMOVED** — interfaces that disappeared
- **CHANGED** — IP address, Status or Protocol differences, shown as `before -> after`

It also handles the two-word status `administratively down` correctly.

## Usage

Requires Python 3.8+.

```bash
python ifdiff.py pre.txt post.txt
```

1. Save the output of `show ip interface brief` before the change (`pre.txt`).
2. Save it again after the change (`post.txt`).
3. Run the script.

Terminal logs from PuTTY or Tera Term can be used as-is: prompt and command lines are skipped automatically.

Sample files are in [`examples/`](examples/). They use documentation address ranges (RFC 5737).

## Notes

- Tested with Cisco IOS-style output. Column layouts differ between platforms; adjust `parse_brief()` if needed.
- Follow your organization's rules and approvals when collecting output from devices.
- **Do not commit real device output** (hostnames, IP addresses, configs) to a public repository.

## How it works

Written up step by step here: _(dev.to article URL)_

## More tools

- Free: **The First 10 Minutes of a Network Incident — Triage Cheat Sheet (PDF)**, plus English templates for incident reports and maintenance runbooks: https://yurunwops.gumroad.com

## License

MIT
