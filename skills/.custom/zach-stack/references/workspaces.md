# Workspace conventions (`zach-stack`)

## Rationale

Use workspaces to separate concerns, reduce coupling, and support agent navigation.

## Typical patterns

- `workspace` for source code organization when multiple modules are expected.
- Separate project for shared data access layer if data feeds multiple components.
- Separate Streamlit app workspace for visualization and UX.
- Keep dependency graphs explicit and directional (core < data < apps).

## Decision matrix

- One module, one team, low coupling pressure: avoid an early workspace split; keep one project and document boundaries.
- Shared data contracts plus multiple consumers (API + jobs + UI): split by boundary and centralize shared contracts/loaders.
- Mixed Python + frontend repo: use explicit module boundaries and a documented command surface before adding more tooling layers.
- Multiple independently released modules: adopt workspaces so commands, dependencies, and ownership are explicit.

## Source-backed notes

### uv workspaces (Python)

- Source: [uv Using Workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)
- Excerpt (short): "Every workspace needs a root..."
- Why it matters for zach-stack: uv workspaces are structured, not just folders with multiple `pyproject.toml` files.
- Practical implication: define a root member and document which commands run at root vs member packages.

- Source: [uv Using Workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)
- Excerpt (short): "`uv run` and `uv sync` operates on the workspace root."
- Why it matters for zach-stack: default command behavior changes after a workspace split.
- Practical implication: add root/member command examples in `Justfile` and `docs/` immediately after introducing a workspace.

### pnpm workspaces (Web / JS)

- Source: [pnpm Workspaces](https://pnpm.io/workspaces)
- Excerpt (short): "A workspace must have a `pnpm-workspace.yaml` file in its root."
- Why it matters for zach-stack: prevents vague workspace recommendations and anchors the minimal required structure.
- Practical implication: add `pnpm-workspace.yaml` as the explicit monorepo boundary when using pnpm workspaces.

- Source: [pnpm Workspaces](https://pnpm.io/workspaces)
- Excerpt (short): "pnpm supports the `workspace:` protocol."
- Why it matters for zach-stack: the `workspace:` protocol reduces ambiguity about local-vs-registry resolution.
- Practical implication: prefer `workspace:` dependencies for internal package links when correctness matters more than convenience.
