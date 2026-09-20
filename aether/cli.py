from __future__ import annotations

import sys
from aether.kernel import AetherKernel


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    goal = " ".join(args) if args else "probe this host and propose which daemons Aether should absorb first"
    print(AetherKernel().run(goal))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
