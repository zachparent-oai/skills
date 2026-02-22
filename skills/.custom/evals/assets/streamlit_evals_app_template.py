from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Eval Runner", layout="wide")


@st.cache_data(show_spinner=False)
def load_dataset(path_text: str) -> pd.DataFrame:
    path = Path(path_text).expanduser()
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)

    if suffix == ".jsonl":
        rows: list[dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                rows.append(json.loads(line))
        return pd.json_normalize(rows)

    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return pd.json_normalize(data)
        if isinstance(data, dict):
            if "rows" in data and isinstance(data["rows"], list):
                return pd.json_normalize(data["rows"])
            return pd.json_normalize([data])

    raise ValueError(f"Unsupported dataset format: {suffix}")


def apply_subset(
    df: pd.DataFrame,
    limit: int,
    sample_seed: int,
    categories: list[str],
) -> pd.DataFrame:
    out = df.copy()

    if categories and "category" in out.columns:
        out = out[out["category"].astype(str).isin(categories)]

    if sample_seed >= 0 and len(out) > 0:
        out = out.sample(frac=1.0, random_state=sample_seed).reset_index(drop=True)

    if limit > 0:
        out = out.head(limit)

    return out.reset_index(drop=True)


def run_eval_harness(rows: pd.DataFrame, run_config: dict[str, Any]) -> pd.DataFrame:
    """
    Replace this stub with your real harness call.

    Recommended patterns:
    - Import and call a project-local Python function that returns row-level results
    - Call a stable CLI wrapper and read the emitted results.jsonl
    """
    results = rows.copy()
    if "id" not in results.columns:
        results["id"] = [f"row-{i:04d}" for i in range(len(results))]

    if "category" not in results.columns:
        results["category"] = "uncategorized"

    # Placeholder columns so the UI works before integration.
    if "output" in results.columns:
        results["output"] = results["output"].astype(str)
    else:
        results["output"] = ""
    results["pass"] = True
    results["score"] = 1.0
    results["failure_reason"] = ""
    results["model"] = run_config["model_id"]
    results["prompt_version"] = run_config["prompt_version"]
    return results


def summarize_results(results: pd.DataFrame) -> dict[str, Any]:
    if len(results) == 0:
        return {"rows": 0, "passes": 0, "pass_rate": 0.0, "avg_score": 0.0}

    passes = int(results["pass"].fillna(False).astype(bool).sum()) if "pass" in results else 0
    pass_rate = passes / len(results)
    avg_score = float(results["score"].mean()) if "score" in results else 0.0
    return {
        "rows": int(len(results)),
        "passes": passes,
        "pass_rate": pass_rate,
        "avg_score": avg_score,
    }


def main() -> None:
    st.title("Eval Runner")
    st.caption("Start with small subsets. Scale up only after the harness is stable.")

    with st.sidebar:
        st.header("Dataset")
        dataset_path = st.text_input("Dataset path", value="evals/datasets/golden.csv")

        load_clicked = st.button("Load dataset", type="primary")

        st.header("Subset")
        limit = st.number_input("Limit rows", min_value=1, max_value=100000, value=10, step=1)
        sample_seed = st.number_input(
            "Sample/shuffle seed (-1 disables)",
            min_value=-1,
            max_value=2_147_483_647,
            value=7,
            step=1,
        )

        st.header("Run config")
        model_id = st.text_input("Model ID", value="replace-with-target-model")
        prompt_version = st.text_input("Prompt version", value="prompt_v1")
        grader_version = st.text_input("Grader version", value="grader_v1")

    if load_clicked:
        try:
            st.session_state["dataset_df"] = load_dataset(dataset_path)
            st.session_state["dataset_path"] = dataset_path
            st.session_state.pop("results_df", None)
            st.success("Dataset loaded.")
        except Exception as exc:  # noqa: BLE001
            st.error(f"Failed to load dataset: {exc}")

    dataset_df = st.session_state.get("dataset_df")
    if dataset_df is None:
        st.info("Load a CSV, JSON, or JSONL dataset to begin.")
        return

    st.subheader("Dataset preview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", len(dataset_df))
    c2.metric("Columns", len(dataset_df.columns))
    c3.metric("Path", st.session_state.get("dataset_path", ""))

    category_options: list[str] = []
    if "category" in dataset_df.columns:
        category_options = sorted(dataset_df["category"].dropna().astype(str).unique().tolist())

    selected_categories = st.multiselect(
        "Categories",
        options=category_options,
        default=[],
        help="Leave empty to include all categories.",
    )

    subset_df = apply_subset(
        dataset_df,
        limit=int(limit),
        sample_seed=int(sample_seed),
        categories=selected_categories,
    )

    st.caption(f"Subset rows selected: {len(subset_df)}")
    st.dataframe(subset_df.head(100), use_container_width=True, height=240)

    run_cols = st.columns([1, 3])
    run_clicked = run_cols[0].button("Run eval", type="primary")
    run_cols[1].caption(
        "Keep this button on small subsets while integrating the harness. "
        "Add a separate full-run flow later."
    )

    if run_clicked:
        run_config = {
            "dataset_path": st.session_state.get("dataset_path", dataset_path),
            "model_id": model_id,
            "prompt_version": prompt_version,
            "grader_version": grader_version,
            "limit": int(limit),
            "sample_seed": int(sample_seed),
            "categories": selected_categories,
        }
        with st.spinner("Running eval harness..."):
            try:
                results_df = run_eval_harness(subset_df, run_config)
                st.session_state["results_df"] = results_df
                st.session_state["run_config"] = run_config
                st.success("Eval run complete.")
            except Exception as exc:  # noqa: BLE001
                st.error(f"Eval run failed: {exc}")

    results_df = st.session_state.get("results_df")
    if results_df is None:
        return

    st.subheader("Results")
    summary = summarize_results(results_df)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rows", summary["rows"])
    m2.metric("Passes", summary["passes"])
    m3.metric("Pass rate", f"{summary['pass_rate']:.1%}")
    m4.metric("Avg score", f"{summary['avg_score']:.3f}")

    if "category" in results_df.columns and "pass" in results_df.columns and len(results_df) > 0:
        by_cat = (
            results_df.assign(pass_num=results_df["pass"].fillna(False).astype(bool).astype(int))
            .groupby("category", dropna=False, as_index=False)
            .agg(pass_rate=("pass_num", "mean"), rows=("pass_num", "size"))
        )
        fig = px.bar(
            by_cat,
            x="category",
            y="pass_rate",
            hover_data=["rows"],
            title="Pass rate by category",
            range_y=[0, 1],
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Run config", expanded=False):
        st.json(st.session_state.get("run_config", {}))

    st.dataframe(results_df, use_container_width=True, height=320)

    if len(results_df) > 0:
        row_index = st.number_input(
            "Inspect row index",
            min_value=0,
            max_value=max(len(results_df) - 1, 0),
            value=0,
            step=1,
        )
        row_data = results_df.iloc[int(row_index)].to_dict()
        st.json(row_data)


if __name__ == "__main__":
    main()
