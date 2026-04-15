import io
from typing import Dict

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Jatropha Farm Evaluation", layout="wide")

# =========================================================
# Jatropha Farm Budget / Yield / Evaluation Tool
# - English only
# - CSV-first design
# - Streamlit Community Cloud friendly
# - Farm-level management
# - Stage-aware model for Year1 / Year2 / Year3 / Year4+
# =========================================================


def clamp(value: float, min_value: float = 0.0, max_value: float = 100.0) -> float:
    return max(min_value, min(max_value, value))


def safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def to_excel_bytes(sheets: Dict[str, pd.DataFrame]) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    output.seek(0)
    return output.read()


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


STAGES = {
    "Year1": {"label": "Year 1", "month_min": 0, "month_max": 12},
    "Year2": {"label": "Year 2", "month_min": 13, "month_max": 24},
    "Year3": {"label": "Year 3", "month_min": 25, "month_max": 36},
    "Year4Plus": {"label": "Year 4+", "month_min": 37, "month_max": 999},
}

DEFAULT_STAGE_YIELD = pd.DataFrame(
    [
        {"stage": "Year1", "annual_yield_target_kg_per_ha": 50, "notes": "Very low / establishment stage"},
        {"stage": "Year2", "annual_yield_target_kg_per_ha": 250, "notes": "Early production stage"},
        {"stage": "Year3", "annual_yield_target_kg_per_ha": 600, "notes": "Growing production stage"},
        {"stage": "Year4Plus", "annual_yield_target_kg_per_ha": 1200, "notes": "Mature production stage"},
    ]
)

DEFAULT_STAGE_WEIGHTS = pd.DataFrame(
    [
        {"stage": "Year1", "yield_weight": 5, "yoy_weight": 0, "budget_weight": 55, "report_weight": 20, "growth_weight": 20, "loss_weight": 0},
        {"stage": "Year2", "yield_weight": 15, "yoy_weight": 20, "budget_weight": 40, "report_weight": 10, "growth_weight": 15, "loss_weight": 0},
        {"stage": "Year3", "yield_weight": 20, "yoy_weight": 30, "budget_weight": 40, "report_weight": 10, "growth_weight": 0, "loss_weight": 0},
        {"stage": "Year4Plus", "yield_weight": 20, "yoy_weight": 25, "budget_weight": 35, "report_weight": 10, "growth_weight": 0, "loss_weight": 10},
    ]
)

DEFAULT_COST_MODEL = pd.DataFrame(
    [
        {"stage": "Year1", "cost_item": "Land Preparation", "annual_standard_php_per_ha": 18000, "seasonality_note": "Pre-planting", "editable": True},
        {"stage": "Year1", "cost_item": "Planting", "annual_standard_php_per_ha": 12000, "seasonality_note": "At establishment", "editable": True},
        {"stage": "Year1", "cost_item": "Replanting", "annual_standard_php_per_ha": 5000, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year1", "cost_item": "Weeding", "annual_standard_php_per_ha": 9000, "seasonality_note": "Repeated", "editable": True},
        {"stage": "Year1", "cost_item": "Fertilizing", "annual_standard_php_per_ha": 7000, "seasonality_note": "Repeated", "editable": True},
        {"stage": "Year1", "cost_item": "Spraying", "annual_standard_php_per_ha": 4000, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year1", "cost_item": "Water", "annual_standard_php_per_ha": 6000, "seasonality_note": "Dry season", "editable": True},
        {"stage": "Year1", "cost_item": "Guard / Monitoring", "annual_standard_php_per_ha": 5000, "seasonality_note": "All year", "editable": True},
        {"stage": "Year1", "cost_item": "Tools / Consumables", "annual_standard_php_per_ha": 3500, "seasonality_note": "All year", "editable": True},
        {"stage": "Year1", "cost_item": "Transport / Hauling", "annual_standard_php_per_ha": 2500, "seasonality_note": "Light", "editable": True},
        {"stage": "Year1", "cost_item": "Repair / Maintenance", "annual_standard_php_per_ha": 2000, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year1", "cost_item": "Outsourcing / Misc.", "annual_standard_php_per_ha": 3000, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year2", "cost_item": "Replanting", "annual_standard_php_per_ha": 4000, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year2", "cost_item": "Weeding", "annual_standard_php_per_ha": 8500, "seasonality_note": "Repeated", "editable": True},
        {"stage": "Year2", "cost_item": "Fertilizing / Refertilizing", "annual_standard_php_per_ha": 9000, "seasonality_note": "Repeated", "editable": True},
        {"stage": "Year2", "cost_item": "Spraying", "annual_standard_php_per_ha": 4500, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year2", "cost_item": "Pruning", "annual_standard_php_per_ha": 3500, "seasonality_note": "Scheduled", "editable": True},
        {"stage": "Year2", "cost_item": "Water", "annual_standard_php_per_ha": 4500, "seasonality_note": "Dry season", "editable": True},
        {"stage": "Year2", "cost_item": "Harvest Labor", "annual_standard_php_per_ha": 5000, "seasonality_note": "Light harvesting", "editable": True},
        {"stage": "Year2", "cost_item": "Transport / Hauling", "annual_standard_php_per_ha": 4000, "seasonality_note": "Seasonal", "editable": True},
        {"stage": "Year2", "cost_item": "Guard / Monitoring", "annual_standard_php_per_ha": 5000, "seasonality_note": "All year", "editable": True},
        {"stage": "Year2", "cost_item": "Tools / Consumables", "annual_standard_php_per_ha": 3500, "seasonality_note": "All year", "editable": True},
        {"stage": "Year2", "cost_item": "Repair / Maintenance", "annual_standard_php_per_ha": 2500, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year2", "cost_item": "Outsourcing / Misc.", "annual_standard_php_per_ha": 3000, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year3", "cost_item": "Weeding", "annual_standard_php_per_ha": 8000, "seasonality_note": "Repeated", "editable": True},
        {"stage": "Year3", "cost_item": "Fertilizing / Refertilizing", "annual_standard_php_per_ha": 10000, "seasonality_note": "Repeated", "editable": True},
        {"stage": "Year3", "cost_item": "Spraying", "annual_standard_php_per_ha": 5000, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year3", "cost_item": "Pruning", "annual_standard_php_per_ha": 4500, "seasonality_note": "Scheduled", "editable": True},
        {"stage": "Year3", "cost_item": "Harvest Labor", "annual_standard_php_per_ha": 9000, "seasonality_note": "Regular harvest", "editable": True},
        {"stage": "Year3", "cost_item": "Transport / Hauling", "annual_standard_php_per_ha": 6500, "seasonality_note": "Seasonal", "editable": True},
        {"stage": "Year3", "cost_item": "Guard / Monitoring", "annual_standard_php_per_ha": 5000, "seasonality_note": "All year", "editable": True},
        {"stage": "Year3", "cost_item": "Tools / Consumables", "annual_standard_php_per_ha": 4000, "seasonality_note": "All year", "editable": True},
        {"stage": "Year3", "cost_item": "Repair / Maintenance", "annual_standard_php_per_ha": 3000, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year3", "cost_item": "Outsourcing / Misc.", "annual_standard_php_per_ha": 3500, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year4Plus", "cost_item": "Weeding", "annual_standard_php_per_ha": 7500, "seasonality_note": "Repeated", "editable": True},
        {"stage": "Year4Plus", "cost_item": "Fertilizing / Refertilizing", "annual_standard_php_per_ha": 11000, "seasonality_note": "Repeated", "editable": True},
        {"stage": "Year4Plus", "cost_item": "Spraying", "annual_standard_php_per_ha": 5500, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year4Plus", "cost_item": "Pruning", "annual_standard_php_per_ha": 5000, "seasonality_note": "Scheduled", "editable": True},
        {"stage": "Year4Plus", "cost_item": "Harvest Labor", "annual_standard_php_per_ha": 14000, "seasonality_note": "Main harvest", "editable": True},
        {"stage": "Year4Plus", "cost_item": "Transport / Hauling", "annual_standard_php_per_ha": 9000, "seasonality_note": "Main harvest", "editable": True},
        {"stage": "Year4Plus", "cost_item": "Guard / Monitoring", "annual_standard_php_per_ha": 5000, "seasonality_note": "All year", "editable": True},
        {"stage": "Year4Plus", "cost_item": "Tools / Consumables", "annual_standard_php_per_ha": 4500, "seasonality_note": "All year", "editable": True},
        {"stage": "Year4Plus", "cost_item": "Repair / Maintenance", "annual_standard_php_per_ha": 3500, "seasonality_note": "As needed", "editable": True},
        {"stage": "Year4Plus", "cost_item": "Outsourcing / Misc.", "annual_standard_php_per_ha": 4000, "seasonality_note": "As needed", "editable": True},
    ]
)

DEFAULT_FARM_MASTER = pd.DataFrame(
    [
        {
            "farm_id": "FARM-001",
            "farm_name": "Sample Farm A",
            "manager_name": "Manager A",
            "area_ha": 10.0,
            "tree_age_months": 18,
            "stage": "Year2",
            "region": "Davao",
            "min_daily_wage_php": 515,
            "regular_daily_workers": 15,
            "approved_budget_php": 680000,
            "previous_year_yield_kg": 1800,
            "previous_year_loss_rate_pct": 5.0,
            "budget_approver": "Mr. Sotomoto",
        }
    ]
)

DEFAULT_MONTHLY_INPUT = pd.DataFrame(
    [
        {
            "farm_id": "FARM-001",
            "month": "2026-01",
            "yield_kg": 100,
            "harvest_loss_rate_pct": 4.0,
            "report_score_manual": 85,
            "survival_rate_pct": 95,
            "replanting_completion_pct": 80,
            "pruning_completion_pct": 70,
            "weeding_completion_pct": 85,
            "budget_overrun_explanation": "",
            "overrun_approved": False,
            "Land Preparation": 0,
            "Planting": 0,
            "Replanting": 5000,
            "Weeding": 8000,
            "Fertilizing": 0,
            "Fertilizing / Refertilizing": 9000,
            "Spraying": 3000,
            "Pruning": 1000,
            "Water": 2000,
            "Harvest Labor": 0,
            "Transport / Hauling": 0,
            "Guard / Monitoring": 3000,
            "Tools / Consumables": 1000,
            "Repair / Maintenance": 0,
            "Outsourcing / Misc.": 0,
        }
    ]
)


def assign_stage_from_months(tree_age_months: int) -> str:
    for stage_code, meta in STAGES.items():
        if meta["month_min"] <= tree_age_months <= meta["month_max"]:
            return stage_code
    return "Year4Plus"


def annual_standard_budget_per_ha(cost_model_df: pd.DataFrame) -> pd.DataFrame:
    return (
        cost_model_df.groupby("stage", as_index=False)["annual_standard_php_per_ha"]
        .sum()
        .rename(columns={"annual_standard_php_per_ha": "annual_standard_budget_php_per_ha"})
    )


def build_farm_budget_reference(farm_df: pd.DataFrame, cost_model_df: pd.DataFrame) -> pd.DataFrame:
    budget_per_ha = annual_standard_budget_per_ha(cost_model_df)
    merged = farm_df.merge(budget_per_ha, on="stage", how="left")
    merged["standard_budget_php"] = merged["annual_standard_budget_php_per_ha"] * merged["area_ha"]
    merged["budget_variance_php"] = merged["approved_budget_php"] - merged["standard_budget_php"]
    merged["budget_variance_pct"] = merged.apply(
        lambda row: safe_div(row["budget_variance_php"], row["standard_budget_php"]) * 100 if row["standard_budget_php"] else 0,
        axis=1,
    )
    return merged


def summarize_monthly_to_annual(monthly_df: pd.DataFrame, cost_model_df: pd.DataFrame) -> pd.DataFrame:
    known_cost_items = cost_model_df["cost_item"].unique().tolist()
    available_cost_cols = [col for col in known_cost_items if col in monthly_df.columns]

    agg_dict = {
        "yield_kg": "sum",
        "harvest_loss_rate_pct": "mean",
        "report_score_manual": "mean",
        "survival_rate_pct": "mean",
        "replanting_completion_pct": "mean",
        "pruning_completion_pct": "mean",
        "weeding_completion_pct": "mean",
        "overrun_approved": "max",
    }
    for col in available_cost_cols:
        agg_dict[col] = "sum"

    annual = monthly_df.groupby("farm_id", as_index=False).agg(agg_dict)
    annual["annual_total_cost_php"] = annual[available_cost_cols].sum(axis=1) if available_cost_cols else 0
    return annual


def merge_annual_data(
    farm_df: pd.DataFrame,
    annual_df: pd.DataFrame,
    yield_targets_df: pd.DataFrame,
    weights_df: pd.DataFrame,
    cost_model_df: pd.DataFrame,
) -> pd.DataFrame:
    base = build_farm_budget_reference(farm_df, cost_model_df)
    merged = base.merge(annual_df, on="farm_id", how="left")
    merged = merged.merge(yield_targets_df, on="stage", how="left")
    merged = merged.merge(weights_df, on="stage", how="left")

    numeric_fill_cols = [
        "yield_kg",
        "harvest_loss_rate_pct",
        "report_score_manual",
        "survival_rate_pct",
        "replanting_completion_pct",
        "pruning_completion_pct",
        "weeding_completion_pct",
        "annual_total_cost_php",
    ]
    for col in numeric_fill_cols:
        if col in merged.columns:
            merged[col] = merged[col].fillna(0)

    merged["yield_kg_per_ha"] = merged.apply(lambda row: safe_div(row["yield_kg"], row["area_ha"]), axis=1)
    merged["cost_php_per_ha"] = merged.apply(lambda row: safe_div(row["annual_total_cost_php"], row["area_ha"]), axis=1)
    merged["yield_target_total_kg"] = merged["annual_yield_target_kg_per_ha"] * merged["area_ha"]
    merged["yield_attainment_pct"] = merged.apply(
        lambda row: safe_div(row["yield_kg"], row["yield_target_total_kg"]) * 100,
        axis=1,
    )
    merged["budget_consumption_pct"] = merged.apply(
        lambda row: safe_div(row["annual_total_cost_php"], row["approved_budget_php"]) * 100,
        axis=1,
    )

    merged["yoy_pct"] = merged.apply(
        lambda row: safe_div(row["yield_kg"] - row["previous_year_yield_kg"], row["previous_year_yield_kg"]) * 100
        if row.get("previous_year_yield_kg", 0) not in [0, None] else 0,
        axis=1,
    )

    merged["yield_score"] = merged["yield_attainment_pct"].apply(lambda x: clamp(x, 0, 120))

    def calc_budget_score(row: pd.Series) -> float:
        approved = row.get("approved_budget_php", 0)
        actual = row.get("annual_total_cost_php", 0)
        overrun_approved = bool(row.get("overrun_approved", False))
        if approved <= 0:
            return 0.0
        if actual <= approved:
            return clamp(100 - abs((approved - actual) / approved) * 20, 70, 110)
        if overrun_approved:
            return 100.0
        overrun_pct = safe_div(actual - approved, approved) * 100
        return clamp(100 - overrun_pct * 2.0, 0, 100)

    merged["budget_score"] = merged.apply(calc_budget_score, axis=1)

    def calc_yoy_score(row: pd.Series) -> float:
        stage = row["stage"]
        yoy = row["yoy_pct"]
        if stage == "Year1":
            return 0.0
        if stage == "Year2":
            return clamp(100 + yoy * 0.5, 50, 120)
        return clamp(100 + yoy * 0.7, 40, 130)

    merged["yoy_score"] = merged.apply(calc_yoy_score, axis=1)
    merged["report_score"] = merged["report_score_manual"].apply(lambda x: clamp(x, 0, 100))

    def calc_growth_score(row: pd.Series) -> float:
        stage = row["stage"]
        if stage not in ["Year1", "Year2"]:
            return 0.0
        components = [
            row.get("survival_rate_pct", 0),
            row.get("replanting_completion_pct", 0),
            row.get("pruning_completion_pct", 0),
            row.get("weeding_completion_pct", 0),
        ]
        valid = [float(x) for x in components if pd.notna(x)]
        return sum(valid) / len(valid) if valid else 0.0

    merged["growth_score"] = merged.apply(calc_growth_score, axis=1)

            def calc_loss_score(row: pd.Series) -> float:
        if row["stage"] != "Year4Plus":
            return 0.0
        return clamp(100 - row.get("harvest_loss_rate_pct", 0) * 5, 0, 100)

    merged["loss_score"] = merged.apply(calc_loss_score, axis=1)

    def calc_final_score(row: pd.Series) -> float:
        return (
            row["yield_score"] * row["yield_weight"]
            + row["yoy_score"] * row["yoy_weight"]
            + row["budget_score"] * row["budget_weight"]
            + row["report_score"] * row["report_weight"]
            + row["growth_score"] * row["growth_weight"]
            + row.get("loss_score", 0) * row.get("loss_weight", 0)
        ) / 100

    merged["final_score"] = merged.apply(calc_final_score, axis=1)
    merged["rating"] = pd.cut(
        merged["final_score"],
        bins=[-1, 59.99, 74.99, 89.99, 200],
        labels=["Needs Improvement", "Fair", "Good", "Excellent"],
    )
    return merged


st.title("Jatropha Farm Budget, Yield, and Evaluation Tool")
st.caption("Farm-level annual evaluation with stage-aware model for Year 1 / Year 2 / Year 3 / Year 4+.")

with st.sidebar:
    st.header("Data Source")
    use_sample = st.toggle("Use sample data", value=True)
    farm_file = st.file_uploader("Upload farm_master.csv", type=["csv"])
    monthly_file = st.file_uploader("Upload monthly_input.csv", type=["csv"])
    cost_file = st.file_uploader("Upload cost_model.csv", type=["csv"])
    yield_file = st.file_uploader("Upload stage_yield_targets.csv", type=["csv"])
    weight_file = st.file_uploader("Upload stage_weights.csv", type=["csv"])

farm_df = DEFAULT_FARM_MASTER.copy() if use_sample or farm_file is None else pd.read_csv(farm_file)
monthly_df = DEFAULT_MONTHLY_INPUT.copy() if use_sample or monthly_file is None else pd.read_csv(monthly_file)
cost_model_df = DEFAULT_COST_MODEL.copy() if use_sample or cost_file is None else pd.read_csv(cost_file)
yield_targets_df = DEFAULT_STAGE_YIELD.copy() if use_sample or yield_file is None else pd.read_csv(yield_file)
weights_df = DEFAULT_STAGE_WEIGHTS.copy() if use_sample or weight_file is None else pd.read_csv(weight_file)

if "stage" not in farm_df.columns and "tree_age_months" in farm_df.columns:
    farm_df["stage"] = farm_df["tree_age_months"].apply(assign_stage_from_months)

if "stage" in farm_df.columns and "tree_age_months" in farm_df.columns:
    farm_df["stage_auto"] = farm_df["tree_age_months"].apply(assign_stage_from_months)


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["1. Settings", "2. Farm Master", "3. Monthly Input", "4. Annual Evaluation", "5. Export"]
)

with tab1:
    st.subheader("Stage Yield Targets")
    edited_yield_targets = st.data_editor(yield_targets_df, use_container_width=True, num_rows="fixed")

    st.subheader("Stage Evaluation Weights")
    edited_weights = st.data_editor(weights_df, use_container_width=True, num_rows="fixed")

    st.subheader("Standard Cost Model (PHP / ha / year)")
    edited_cost_model = st.data_editor(cost_model_df, use_container_width=True, num_rows="dynamic")
    st.subheader("Standard Annual Budget per ha")
    st.dataframe(annual_standard_budget_per_ha(edited_cost_model), use_container_width=True)

with tab2:
    st.subheader("Farm Master")
    edited_farm_df = st.data_editor(farm_df, use_container_width=True, num_rows="dynamic")
    if "tree_age_months" in edited_farm_df.columns:
        preview_df = edited_farm_df.copy()
        preview_df["stage_from_age"] = preview_df["tree_age_months"].apply(assign_stage_from_months)
        st.caption("Stage preview from tree age months")
        st.dataframe(preview_df, use_container_width=True)
    else:
        preview_df = edited_farm_df.copy()

with tab3:
    st.subheader("Monthly Input")
    edited_monthly_df = st.data_editor(monthly_df, use_container_width=True, num_rows="dynamic")
    known_cost_items = edited_cost_model["cost_item"].unique().tolist()
    missing_cols = [item for item in known_cost_items if item not in edited_monthly_df.columns]
    if missing_cols:
        st.warning("Missing monthly cost columns: " + ", ".join(missing_cols))

with tab4:
    annual_df = summarize_monthly_to_annual(edited_monthly_df, edited_cost_model)
    result_df = merge_annual_data(preview_df, annual_df, edited_yield_targets, edited_weights, edited_cost_model)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("No. of farms", len(result_df))
    c2.metric("Avg final score", f"{result_df['final_score'].mean():.1f}")
    c3.metric("Avg yield / ha", f"{result_df['yield_kg_per_ha'].mean():,.1f} kg")
    c4.metric("Avg cost / ha", f"PHP {result_df['cost_php_per_ha'].mean():,.0f}")

    st.subheader("Annual Evaluation Table")
    st.dataframe(result_df, use_container_width=True)

    st.subheader("Budget Reference by Farm")
    st.dataframe(build_farm_budget_reference(preview_df, edited_cost_model), use_container_width=True)

with tab5:
    annual_df = summarize_monthly_to_annual(edited_monthly_df, edited_cost_model)
    result_df = merge_annual_data(preview_df, annual_df, edited_yield_targets, edited_weights, edited_cost_model)
    excel_bytes = to_excel_bytes(
        {
            "farm_master": preview_df,
            "monthly_input": edited_monthly_df,
            "cost_model": edited_cost_model,
            "stage_yield_targets": edited_yield_targets,
            "stage_weights": edited_weights,
            "annual_result": result_df,
        }
    )
    st.download_button(
        label="Download Excel",
        data=excel_bytes,
        file_name="jatropha_farm_evaluation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.download_button(
        label="Download Annual Result CSV",
        data=df_to_csv_bytes(result_df),
        file_name="annual_result.csv",
        mime="text/csv",
    )
    st.info("PDF export is not implemented in this first version.")

with st.expander("Recommended CSV columns"):
    st.markdown(
        """
**farm_master.csv**
- farm_id
- farm_name
- manager_name
- area_ha
- tree_age_months
- stage
- region
- min_daily_wage_php
- regular_daily_workers
- approved_budget_php
- previous_year_yield_kg
- previous_year_loss_rate_pct
- budget_approver

**monthly_input.csv**
- farm_id
- month
- yield_kg
- harvest_loss_rate_pct
- report_score_manual
- survival_rate_pct
- replanting_completion_pct
- pruning_completion_pct
- weeding_completion_pct
- budget_overrun_explanation
- overrun_approved
- one column for each cost item

**cost_model.csv**
- stage
- cost_item
- annual_standard_php_per_ha
- seasonality_note
- editable

**stage_yield_targets.csv**
- stage
- annual_yield_target_kg_per_ha
- notes

**stage_weights.csv**
- stage
- yield_weight
- yoy_weight
- budget_weight
- report_weight
- growth_weight
- loss_weight
        """
    )
