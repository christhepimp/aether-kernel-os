# Aether architecture

The AI *is* the OS kernel of this project. Hardware still needs a real kernel (Linux for now).

## Modules

| Module | Job |
|---|---|
| Scheduler | Turns goals into time-sliced agent tasks |
| Memory | Working buffer + episodic log + optional vector store later |
| Storage | Named artifacts, not raw POSIX by default |
| Tools | Capability-gated syscalls (inspect host, read file, run allowlisted command) |
| Policy | Deny-by-default for destructive actions |
| IPC | Message bus between agents |

## Process model

An **agent** is a process from Aether's point of view:

- goal string
- priority
- memory handle
- tool capabilities
- budget (steps / tokens / wall time)

The host Linux process that runs `python -m aether` is just the *bootstrap*. Later this becomes a systemd unit or an Android init service.

## Why Linux stays underneath (for now)

Drivers, filesystems, scheduling of CPU threads, and Android binder already exist. Replacing them before we own userland is how hobby kernels die. See `KERNEL.md`.
