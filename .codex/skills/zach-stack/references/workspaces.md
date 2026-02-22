# Workspace conventions (`zach-stack`)

## Rationale

Use workspaces to separate concerns, reduce coupling, and support agent navigation.

## Typical patterns

- `workspace` for source code organization when multiple modules are expected.
- Separate project for shared data access layer if data feeds multiple components.
- Separate Streamlit app workspace for visualization and UX.
- Keep dependency graphs explicit and directional (core < data < apps).
