# Research hosts

Goal: a machine (or VM) where you have root, a Linux-family process tree, and a place to park the Aether daemon.

## 1. Waydroid (recommended on Linux)

Waydroid is not a classic emulator. It is Android userland in an LXC container on *your* kernel. That is the shortest path into "Linux inside Android."

- Project: https://github.com/waydroid/waydroid
- Needs: Linux host, Wayland or XWayland, sudo for container init
- Inside-Android root: optional Magisk via community `waydroid_script`

```bash
sudo waydroid shell
uname -a
cat /proc/version
ps -A | head
mount | head
```

Host-side you already *are* Linux. Aether should start as a host systemd service that can also enter the container namespace.

## 2. Genymotion Desktop

Commercial/personal Android VM. Root can be enabled in device settings / Advanced Developer Tools on supported images. Older Android images often ship already rooted.

Docs: https://docs.genymotion.com/desktop/Using_root_access

```bash
adb devices
adb root
adb shell
id
```

Use this if you want a polished Android *phone* UI and a rooted `adb shell` without building containers.

## 3. Official Android Emulator + Magisk

Harder root story, best Google compatibility. Patch a system image, boot an AVD, confirm `su`.

## 4. Bliss OS in QEMU/KVM

Treat Android as the guest OS, not an app runtime. Good when you want to replace more of the stack later (custom init, custom launcher) without fighting a phone skin.

## Safety

- Root on an emulator/VM you own is fine. Do not use this writeup to attack devices you do not own.
- Never commit Magisk-patched proprietary images here.
- Aether tools that run shell commands must stay allowlisted.
