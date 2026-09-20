# Aether Kernel OS

**The OS itself is the AI.** Not a chat app on Linux. A control plane that treats goals as processes, tools as syscalls, and memory as a first-class subsystem — then slowly takes over Linux userland instead of pretending we can rip the kernel out in one night.

> Status: architecture + host research + runnable userland prototype.
> Not a drop-in Linux replacement. That claim would be a lie.

Repo: https://github.com/christhepimp/aether-kernel-os

---

## What this project actually is

You asked for:

1. A GitHub repo
2. A rooted Android / Linux research host
3. Get *inside* the Linux userspace on that host
4. Start replacing Linux with an OS we write — incrementally
5. The OS is AI: the scheduler, memory, and policy are agents

What nobody can honestly ship in one commit:

- A from-scratch kernel that boots on phones and PCs and replaces Linux tomorrow
- Magically rewriting Android's kernel from an emulator GUI

Real OS replacement is **strangler-fig**: keep a Linux (or Android) kernel for drivers and hardware, replace init, package manager, windowing, and policy with Aether services until the old userland is optional.

---

## Research hosts (rooted Android / Linux)

| Host | What it is | Root | Why it fits |
|---|---|---|---|
| **Waydroid** | Android 13 (LineageOS) in an LXC container on your Linux kernel | Host sudo + optional Magisk inside Android | Best for seeing Linux from both sides. Android userland shares the host kernel. |
| **Genymotion Desktop** | VirtualBox/QEMU Android VM | Built-in root toggle on many images | Clean rooted shell via adb. |
| **Android Studio AVD + Magisk** | Official emulator | Magisk-patched system image | Standard Google images. |
| **Bliss OS in QEMU/KVM** | Full Android-x86 OS | Typical Android-x86 / Magisk path | Closest to a real OS VM you can dual-boot later. |

See `docs/HOSTS.md`.

---

## Architecture

```
Agents / Apps
    |
AETHER KERNEL   scheduler · memory · storage · tools · policy · ipc
    |
Compatibility   Linux syscalls, Android binder
    |
Host kernel     Linux in Waydroid / Genymotion / Bliss / QEMU
```

---

## Replacement ladder

1. Observe — rooted shell, process map, mounts, cgroups
2. Overlay — Aether daemon runs beside Android/Linux init
3. Intercept — files, net, packages go through Aether policy
4. Replace userland — settings, launcher, package manager become agents
5. Shrink the host — keep Linux kernel + drivers; drop unused daemons
6. Optional later — new kernel only after userland is ours

---

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m aether.cli "probe this host and propose which daemons Aether should absorb first"
```

---

## License

Apache-2.0.
