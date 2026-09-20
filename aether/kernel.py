from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List
import time
import uuid


@dataclass
class Memory:
    working: str = ""
    episodes: List[str] = field(default_factory=list)

    def remember(self, event: str) -> None:
        self.episodes.append(event)
        if len(self.episodes) > 200:
            self.episodes = self.episodes[-200:]


@dataclass
class Agent:
    goal: str
    priority: int = 100
    capabilities: List[str] = field(default_factory=lambda: ["inspect"])
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    memory: Memory = field(default_factory=Memory)
    done: bool = False
    last_output: str = ""


class Policy:
    blocked_tokens = ("rm -rf", "mkfs", "dd if=", ":(){", "shutdown", "reboot")

    def allow(self, capability: str, payload: str) -> bool:
        low = payload.lower()
        if any(tok in low for tok in self.blocked_tokens):
            return False
        return capability in {"inspect", "read", "echo"}


class ToolBus:
    def __init__(self) -> None:
        self._tools: Dict[str, Callable[[str], str]] = {}

    def register(self, name: str, fn: Callable[[str], str]) -> None:
        self._tools[name] = fn

    def call(self, name: str, payload: str) -> str:
        if name not in self._tools:
            return f"unknown tool: {name}"
        return self._tools[name](payload)


class AetherKernel:
    def __init__(self) -> None:
        self.agents: List[Agent] = []
        self.policy = Policy()
        self.tools = ToolBus()
        self._register_builtin_tools()

    def _register_builtin_tools(self) -> None:
        self.tools.register("echo", lambda p: p)
        self.tools.register("inspect", self._inspect_host)

    def _inspect_host(self, _payload: str) -> str:
        import os
        import platform

        bits = [
            f"system={platform.system()}",
            f"release={platform.release()}",
            f"python={platform.python_version()}",
            f"cwd={os.getcwd()}",
            f"pid={os.getpid()}",
        ]
        return "\n".join(bits)

    def spawn(self, goal: str, priority: int = 100) -> Agent:
        agent = Agent(goal=goal, priority=priority)
        agent.memory.working = goal
        self.agents.append(agent)
        return agent

    def tick(self, agent: Agent) -> str:
        if agent.done:
            return agent.last_output
        goal = agent.goal.lower()
        if "process" in goal or "daemon" in goal or "probe" in goal or "host" in goal:
            cap = "inspect"
            if cap not in agent.capabilities or not self.policy.allow(cap, goal):
                out = "policy denied inspect"
            else:
                host = self.tools.call("inspect", goal)
                out = (
                    "Aether probe\n"
                    f"{host}\n\n"
                    "Absorb-first candidates (userland, not kernel):\n"
                    "- package manager / app store policy\n"
                    "- settings / preference daemon\n"
                    "- launcher / window manager\n"
                    "- notification / intent router\n"
                    "Keep underneath: Linux kernel, drivers, init, binder.\n"
                )
        else:
            out = (
                "Aether accepted goal as a process.\n"
                f"goal={agent.goal}\n"
                "Next: bind tools, then overlay this daemon on a rooted host.\n"
            )
        agent.memory.remember(out)
        agent.last_output = out
        agent.done = True
        return out

    def run(self, goal: str) -> str:
        agent = self.spawn(goal)
        started = time.time()
        out = self.tick(agent)
        return f"[{agent.id} {time.time() - started:.3f}s]\n{out}"
