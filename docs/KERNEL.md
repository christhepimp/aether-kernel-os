# Kernel track

"Replace Linux" is the destination, not the first commit.

## What people mean vs what works

- **Wrong:** download an Android emulator, open a root shell, delete the Linux kernel, write a new OS in the same afternoon.
- **Right:** keep the host kernel as a hardware abstraction, replace every *policy* daemon above it, then consider a custom kernel when the ABI we need is small.

## Later options (not started)

- Linux kernel fork with Aether as pid 1 userspace only
- seL4 + Linux compatibility VM for leftover apps
- Unikernel for a single-purpose AI appliance

None of those belong in the prototype until `aether/` can supervise a real host without catching fire.
