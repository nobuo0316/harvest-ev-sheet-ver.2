import io
from typing import Dict

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Jatropha Farm Evaluation", layout="wide")

# =========================================================
# Jatropha Farm Budget / Yield / Evaluation Tool
# Bilingual UI version (EN / JP)
# - Farm-level annual evaluation
# - Cost input uses LONG format (farm_id, month, cost_item, amount)
# - Streamlit-friendly form UI
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


LANG_OPTIONS = {
    "English / 日本語": "BOTH",
    "English": "EN",
    "日本語": "JP",
}

LABELS = {
    "app_title": {"EN": "Jatropha Farm Budget, Yield, and Evaluation Tool", "JP": "ジャトロファ農場 予算・収量・評価ツール"},
    "app_caption": {"EN": "UI-first version: monthly costs are entered line by line.", "JP": "入力しやすさ重視版：月次コストは1行ずつ入力します。"},
    "data_source": {"EN": "Data Source", "JP": "データソース"},
    "use_sample": {"EN": "Use sample data", "JP": "サンプルデータを使用"},
    "upload_farm": {"EN": "Upload farm_master.csv", "JP": "farm_master.csv をアップロード"},
    "upload_metrics": {"EN": "Upload monthly_metrics.csv", "JP": "monthly_metrics.csv をアップロード"},
    "upload_costs": {"EN": "Upload monthly_costs.csv", "JP": "monthly_costs.csv をアップロード"},
    "upload_cost_model": {"EN": "Upload cost_model.csv", "JP": "cost_model.csv をアップロード"},
    "upload_targets": {"EN": "Upload stage_yield_targets.csv", "JP": "stage_yield_targets.csv をアップロード"},
    "upload_weights": {"EN": "Upload stage_weights.csv", "JP": "stage_weights.csv をアップロード"},
    "settings": {"EN": "Settings", "JP": "設定"},
    "farm_master": {"EN": "Farm Master", "JP": "農場マスタ"},
    "monthly_metrics": {"EN": "Monthly Metrics", "JP": "月次指標"},
    "monthly_costs": {"EN": "Monthly Costs", "JP": "月次コスト"},
    "annual_evaluation": {"EN": "Annual Evaluation", "JP": "年次評価"},
    "export": {"EN": "Export", "JP": "出力"},
    "stage_yield_targets": {"EN": "Stage Yield Targets", "JP": "樹齢別標準収量"},
    "stage_weights": {"EN": "Stage Evaluation Weights", "JP": "樹齢別評価ウェイト"},
    "cost_model": {"EN": "Standard Cost Model (PHP / ha / year)", "JP": "標準コストモデル（PHP / ha / 年）"},
    "standard_budget": {"EN": "Standard Annual Budget per ha", "JP": "1haあたり標準年間予算"},
    "stage_preview": {"EN": "Stage preview from tree age months", "JP": "樹齢月数からのステージ自動判定"},
    "farm": {"EN": "Farm", "JP": "農場"},
    "month": {"EN": "Month (YYYY-MM)", "JP": "月 (YYYY-MM)"},
    "yield_kg": {"EN": "Yield (kg)", "JP": "収量 (kg)"},
    "loss_rate": {"EN": "Harvest loss rate (%)", "JP": "収穫ロス率 (%)"},
    "report_score": {"EN": "Report score", "JP": "報告評価"},
    "overrun_approved": {"EN": "Budget overrun approved", "JP": "予算超過承認済み"},
    "survival_rate": {"EN": "Survival rate (%)", "JP": "生存率 (%)"},
    "replanting_completion": {"EN": "Replanting completion (%)", "JP": "補植完了率 (%)"},
    "pruning_completion": {"EN": "Pruning completion (%)", "JP": "剪定完了率 (%)"},
    "weeding_completion": {"EN": "Weeding completion (%)", "JP": "除草完了率 (%)"},
    "overrun_explanation": {"EN": "Budget overrun explanation", "JP": "予算超過の説明"},
    "add_monthly_metrics": {"EN": "Add monthly metrics", "JP": "月次指標を追加"},
    "cost_item": {"EN": "Cost item", "JP": "費目"},
    "amount_php": {"EN": "Amount (PHP)", "JP": "金額 (PHP)"},
    "notes": {"EN": "Notes", "JP": "備考"},
    "add_cost_line": {"EN": "Add cost line", "JP": "コスト行を追加"},
    "metrics_added": {"EN": "Monthly metrics added.", "JP": "月次指標を追加しました。"},
    "cost_added": {"EN": "Cost line added.", "JP": "コスト行を追加しました。"},
    "quick_summary": {"EN": "Quick Summary", "JP": "簡易集計"},
    "no_farms": {"EN": "No. of farms", "JP": "農場数"},
    "avg_final_score": {"EN": "Avg final score", "JP": "平均最終スコア"},
    "avg_yield_per_ha": {"EN": "Avg yield / ha", "JP": "平均収量 / ha"},
    "avg_cost_per_ha": {"EN": "Avg cost / ha", "JP": "平均コスト / ha"},
    "annual_eval_table": {"EN": "Annual Evaluation Table", "JP": "年次評価一覧"},
    "monthly_cost_pivot": {"EN": "Monthly Cost Pivot", "JP": "月次コスト ピボット"},
    "download_excel": {"EN": "Download Excel", "JP": "Excelをダウンロード"},
    "download_metrics_csv": {"EN": "Download monthly_metrics.csv", "JP": "monthly_metrics.csv をダウンロード"},
    "download_costs_csv": {"EN": "Download monthly_costs.csv", "JP": "monthly_costs.csv をダウンロード"},
    "download_annual_csv": {"EN": "Download annual_result.csv", "JP": "annual_result.csv をダウンロード"},
    "pdf_not_implemented": {"EN": "PDF export is not implemented in this version.", "JP": "この版では PDF 出力は未実装です。"},
    "recommended_csv": {"EN": "Recommended CSV columns", "JP": "推奨CSV列"},
}

COST_ITEM_JP = {
    "Land Preparation": "土地整備",
    "Planting": "植付",
    "Replanting": "補植",
    "Weeding": "除草",
    "Fertilizing": "施肥",
    "Fertilizing / Refertilizing": "施肥 / 追肥",
    "Spraying": "農薬散布",
    "Water": "散水",
    "Pruning": "剪定",
    "Harvest Labor": "収穫作業",
    "Transport / Hauling": "運搬",
    "Guard / Monitoring": "警備 / モニタリング",
    "Tools / Consumables": "工具 / 消耗品",
    "Repair / Maintenance": "修繕 / 保守",
    "Outsourcing / Misc.": "外注 / 雑費",
}

STAGE_JP = {
    "Year1": "初年次",
    "Year2": "2年目",
    "Year3": "3年目",
    "Year4Plus": "4年目以降",
}


def tr(key: str) -> str:
    mode = st.session_state.get("lang_mode", "BOTH")
    item = LABELS.get(key, {"EN": key, "JP": key})
    if mode == "EN":
        return item["EN"]
    if mode == "JP":
        return item["JP"]
    return f"{item['EN']} / {item['JP']}"



def display_cost_item(item: str) -> str:
    mode = st.session_state.get("lang_mode", "BOTH")
    jp = COST_ITEM_JP.get(item, item)
    if mode == "EN":
        return item
    if mode == "JP":
        return jp
    return f"{item} / {jp}"



def display_stage(stage: str) -> str:
    mode = st.session_state.get("lang_mode", "BOTH")
    jp = STAGE_JP.get(stage, stage)
    if mode == "EN":
        return stage
    if mode == "JP":
        return jp
    return f"{stage} / {jp}"


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

DEFAULT_MONTHLY_METRICS = pd.DataFrame(
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
        }
    ]
)

DEFAULT_MONTHLY_COSTS = pd.DataFrame(
    [
        {"farm_id": "FARM-001", "month": "2026-01", "cost_item": "Weeding", "amount_php": 8000, "notes": ""},
        {"farm_id": "FARM-001", "month": "2026-01", "cost_item": "Fertilizing / Refertilizing", "amount_php": 9000, "notes": ""},
        {"farm_id": "FARM-001", "month": "2026-01", "cost_item": "Spraying", "amount_php": 3000, "notes": ""},
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



def summarize_monthly_costs(monthly_costs_df: pd.DataFrame) -> pd.DataFrame:
    if monthly_costs_df.empty:
        return pd.DataFrame(columns=["farm_id", "annual_total_cost_php"])
    annual_cost = (
        monthly_costs_df.groupby("farm_id", as_index=False)["amount_php"]
        .sum()
        .rename(columns={"amount_php": "annual_total_cost_php"})
    )
    return annual_cost



def summarize_monthly_metrics(monthly_metrics_df: pd.DataFrame) -> pd.DataFrame:
    if monthly_metrics_df.empty:
        return pd.DataFrame(columns=[
            "farm_id", "yield_kg", "harvest_loss_rate_pct", "report_score_manual",
            "survival_rate_pct", "replanting_completion_pct", "pruning_completion_pct",
            "weeding_completion_pct", "overrun_approved"
        ])

    annual_metrics = monthly_metrics_df.groupby("farm_id", as_index=False).agg(
        {
            "yield_kg": "sum",
            "harvest_loss_rate_pct": "mean",
            "report_score_manual": "mean",
            "survival_rate_pct": "mean",
            "replanting_completion_pct": "mean",
            "pruning_completion_pct": "mean",
            "weeding_completion_pct": "mean",
            "overrun_approved": "max",
        }
    )
    return annual_metrics



def monthly_cost_pivot(monthly_costs_df: pd.DataFrame) -> pd.DataFrame:
    if monthly_costs_df.empty:
        return pd.DataFrame(columns=["farm_id", "month", "cost_item", "amount_php"])
    pivot_df = monthly_costs_df.pivot_table(
        index=["farm_id", "month"],
        columns="cost_item",
        values="amount_php",
        aggfunc="sum",
        fill_value=0,
    ).reset_index()
    pivot_df.columns.name = None
    return pivot_df



def merge_annual_data(
    farm_df: pd.DataFrame,
    annual_metrics_df: pd.DataFrame,
    annual_cost_df: pd.DataFrame,
    yield_targets_df: pd.DataFrame,
    weights_df: pd.DataFrame,
    cost_model_df: pd.DataFrame,
) -> pd.DataFrame:
    base = build_farm_budget_reference(farm_df, cost_model_df)
    merged = base.merge(annual_metrics_df, on="farm_id", how="left")
    merged = merged.merge(annual_cost_df, on="farm_id", how="left")
    merged = merged.merge(yield_targets_df, on="stage", how="left")
    merged = merged.merge(weights_df, on="stage", how="left")

    numeric_fill_cols = [
        "yield_kg", "harvest_loss_rate_pct", "report_score_manual", "survival_rate_pct",
        "replanting_completion_pct", "pruning_completion_pct", "weeding_completion_pct",
        "annual_total_cost_php",
    ]
    for col in numeric_fill_cols:
        if col in merged.columns:
            merged[col] = merged[col].fillna(0)

    merged["yield_kg_per_ha"] = merged.apply(lambda row: safe_div(row["yield_kg"], row["area_ha"]), axis=1)
    merged["cost_php_per_ha"] = merged.apply(lambda row: safe_div(row["annual_total_cost_php"], row["area_ha"]), axis=1)
    merged["yield_target_total_kg"] = merged["annual_yield_target_kg_per_ha"] * merged["area_ha"]
    merged["yield_attainment_pct"] = merged.apply(lambda row: safe_div(row["yield_kg"], row["yield_target_total_kg"]) * 100, axis=1)
    merged["budget_consumption_pct"] = merged.apply(lambda row: safe_div(row["annual_total_cost_php"], row["approved_budget_php"]) * 100, axis=1)

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
        if row["stage"] not in ["Year1", "Year2"]:
            return 0.0
        components = [
            row.get("survival_rate_pct", 0),
            row.get("replanting_completion_pct", 0),
            row.get("pruning_completion_pct", 0),
            row.get("weeding_completion_pct", 0),
        ]
        return sum(components) / len(components)

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
            + row["loss_score"] * row["loss_weight"]
        ) / 100

    merged["final_score"] = merged.apply(calc_final_score, axis=1)
    merged["rating"] = pd.cut(
        merged["final_score"],
        bins=[-1, 59.99, 74.99, 89.99, 200],
        labels=["Needs Improvement", "Fair", "Good", "Excellent"],
    )
    return merged


with st.sidebar:
    st.session_state["lang_mode"] = LANG_OPTIONS[
        st.selectbox("Language / 言語", list(LANG_OPTIONS.keys()), index=0)
    ]
    st.header(tr("data_source"))
    use_sample = st.toggle(tr("use_sample"), value=True)
    farm_file = st.file_uploader(tr("upload_farm"), type=["csv"])
    metrics_file = st.file_uploader(tr("upload_metrics"), type=["csv"])
    costs_file = st.file_uploader(tr("upload_costs"), type=["csv"])
    cost_model_file = st.file_uploader(tr("upload_cost_model"), type=["csv"])
    yield_file = st.file_uploader(tr("upload_targets"), type=["csv"])
    weight_file = st.file_uploader(tr("upload_weights"), type=["csv"])

st.title(tr("app_title"))
st.caption(tr("app_caption"))

farm_df = DEFAULT_FARM_MASTER.copy() if use_sample or farm_file is None else pd.read_csv(farm_file)
monthly_metrics_df = DEFAULT_MONTHLY_METRICS.copy() if use_sample or metrics_file is None else pd.read_csv(metrics_file)
monthly_costs_df = DEFAULT_MONTHLY_COSTS.copy() if use_sample or costs_file is None else pd.read_csv(costs_file)
cost_model_df = DEFAULT_COST_MODEL.copy() if use_sample or cost_model_file is None else pd.read_csv(cost_model_file)
yield_targets_df = DEFAULT_STAGE_YIELD.copy() if use_sample or yield_file is None else pd.read_csv(yield_file)
weights_df = DEFAULT_STAGE_WEIGHTS.copy() if use_sample or weight_file is None else pd.read_csv(weight_file)

if "stage" not in farm_df.columns and "tree_age_months" in farm_df.columns:
    farm_df["stage"] = farm_df["tree_age_months"].apply(assign_stage_from_months)

if "monthly_costs_df" not in st.session_state:
    st.session_state.monthly_costs_df = monthly_costs_df.copy()
if "monthly_metrics_df" not in st.session_state:
    st.session_state.monthly_metrics_df = monthly_metrics_df.copy()

cost_item_options = sorted(cost_model_df["cost_item"].unique().tolist())
farm_options = farm_df["farm_id"].tolist()


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        f"1. {tr('settings')}",
        f"2. {tr('farm_master')}",
        f"3. {tr('monthly_metrics')}",
        f"4. {tr('monthly_costs')}",
        f"5. {tr('annual_evaluation')}",
        f"6. {tr('export')}",
    ]
)

with tab1:
    st.subheader(tr("stage_yield_targets"))
    edited_yield_targets = st.data_editor(yield_targets_df, use_container_width=True, num_rows="fixed")

    st.subheader(tr("stage_weights"))
    edited_weights = st.data_editor(weights_df, use_container_width=True, num_rows="fixed")

    st.subheader(tr("cost_model"))
    cost_model_view = cost_model_df.copy()
    cost_model_view["stage_display"] = cost_model_view["stage"].map(display_stage)
    cost_model_view["cost_item_display"] = cost_model_view["cost_item"].map(display_cost_item)
    edited_cost_model = st.data_editor(cost_model_view, use_container_width=True, num_rows="dynamic")
    if "stage_display" in edited_cost_model.columns:
        edited_cost_model = edited_cost_model.drop(columns=["stage_display"])
    if "cost_item_display" in edited_cost_model.columns:
        edited_cost_model = edited_cost_model.drop(columns=["cost_item_display"])

    st.subheader(tr("standard_budget"))
    budget_df = annual_standard_budget_per_ha(edited_cost_model).copy()
    budget_df["stage_display"] = budget_df["stage"].map(display_stage)
    st.dataframe(budget_df, use_container_width=True)

with tab2:
    st.subheader(tr("farm_master"))
    edited_farm_df = st.data_editor(farm_df, use_container_width=True, num_rows="dynamic")
    if "tree_age_months" in edited_farm_df.columns:
        preview_df = edited_farm_df.copy()
        preview_df["stage_from_age"] = preview_df["tree_age_months"].apply(assign_stage_from_months)
        preview_df["stage_from_age_display"] = preview_df["stage_from_age"].map(display_stage)
        st.caption(tr("stage_preview"))
        st.dataframe(preview_df, use_container_width=True)
    else:
        preview_df = edited_farm_df.copy()

with tab3:
    st.subheader(tr("monthly_metrics"))
    with st.form("metrics_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        farm_id = c1.selectbox(tr("farm"), farm_options, key="metrics_farm")
        month = c2.text_input(tr("month"), value="2026-01")
        yield_kg = c3.number_input(tr("yield_kg"), min_value=0.0, value=0.0, step=10.0)

        c4, c5, c6 = st.columns(3)
        loss_rate = c4.number_input(tr("loss_rate"), min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        report_score = c5.number_input(tr("report_score"), min_value=0.0, max_value=100.0, value=85.0, step=1.0)
        overrun_approved = c6.checkbox(tr("overrun_approved"))

        c7, c8, c9, c10 = st.columns(4)
        survival_rate = c7.number_input(tr("survival_rate"), min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        replanting_completion = c8.number_input(tr("replanting_completion"), min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        pruning_completion = c9.number_input(tr("pruning_completion"), min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        weeding_completion = c10.number_input(tr("weeding_completion"), min_value=0.0, max_value=100.0, value=0.0, step=1.0)

        explanation = st.text_input(tr("overrun_explanation"))
        add_metrics = st.form_submit_button(tr("add_monthly_metrics"))

        if add_metrics:
            new_row = pd.DataFrame([
                {
                    "farm_id": farm_id,
                    "month": month,
                    "yield_kg": yield_kg,
                    "harvest_loss_rate_pct": loss_rate,
                    "report_score_manual": report_score,
                    "survival_rate_pct": survival_rate,
                    "replanting_completion_pct": replanting_completion,
                    "pruning_completion_pct": pruning_completion,
                    "weeding_completion_pct": weeding_completion,
                    "budget_overrun_explanation": explanation,
                    "overrun_approved": overrun_approved,
                }
            ])
            st.session_state.monthly_metrics_df = pd.concat([st.session_state.monthly_metrics_df, new_row], ignore_index=True)
            st.success(tr("metrics_added"))

    st.dataframe(st.session_state.monthly_metrics_df, use_container_width=True)

with tab4:
    st.subheader(tr("monthly_costs"))
    cost_item_display_map = {display_cost_item(item): item for item in cost_item_options}
    with st.form("cost_form", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        farm_id = c1.selectbox(tr("farm"), farm_options, key="cost_farm")
        month = c2.text_input(tr("month"), value="2026-01", key="cost_month")
        cost_item_display_value = c3.selectbox(tr("cost_item"), list(cost_item_display_map.keys()))
        amount_php = c4.number_input(tr("amount_php"), min_value=0.0, value=0.0, step=100.0)
        notes = st.text_input(tr("notes"))
        add_cost = st.form_submit_button(tr("add_cost_line"))

        if add_cost:
            new_row = pd.DataFrame([
                {
                    "farm_id": farm_id,
                    "month": month,
                    "cost_item": cost_item_display_map[cost_item_display_value],
                    "amount_php": amount_php,
                    "notes": notes,
                }
            ])
            st.session_state.monthly_costs_df = pd.concat([st.session_state.monthly_costs_df, new_row], ignore_index=True)
            st.success(tr("cost_added"))

    c1, c2 = st.columns([2, 1])
    with c1:
        cost_view_df = st.session_state.monthly_costs_df.copy()
        if not cost_view_df.empty:
            cost_view_df["cost_item_display"] = cost_view_df["cost_item"].map(display_cost_item)
        st.dataframe(cost_view_df, use_container_width=True)
    with c2:
        st.subheader(tr("quick_summary"))
        if not st.session_state.monthly_costs_df.empty:
            summary = (
                st.session_state.monthly_costs_df.groupby("cost_item", as_index=False)["amount_php"]
                .sum()
                .sort_values("amount_php", ascending=False)
            )
            summary["cost_item_display"] = summary["cost_item"].map(display_cost_item)
            st.dataframe(summary, use_container_width=True)

with tab5:
    annual_metrics_df = summarize_monthly_metrics(st.session_state.monthly_metrics_df)
    annual_cost_df = summarize_monthly_costs(st.session_state.monthly_costs_df)
    result_df = merge_annual_data(preview_df, annual_metrics_df, annual_cost_df, edited_yield_targets, edited_weights, edited_cost_model)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(tr("no_farms"), len(result_df))
    c2.metric(tr("avg_final_score"), f"{result_df['final_score'].mean():.1f}")
    c3.metric(tr("avg_yield_per_ha"), f"{result_df['yield_kg_per_ha'].mean():,.1f} kg")
    c4.metric(tr("avg_cost_per_ha"), f"PHP {result_df['cost_php_per_ha'].mean():,.0f}")

    st.subheader(tr("annual_eval_table"))
    display_cols = [
        "farm_id", "farm_name", "manager_name", "area_ha", "tree_age_months", "stage",
        "approved_budget_php", "standard_budget_php", "annual_total_cost_php", "budget_consumption_pct",
        "yield_kg", "yield_kg_per_ha", "annual_yield_target_kg_per_ha", "yield_attainment_pct",
        "previous_year_yield_kg", "yoy_pct", "harvest_loss_rate_pct", "report_score",
        "growth_score", "loss_score", "budget_score", "yield_score", "yoy_score", "final_score", "rating"
    ]
    existing_cols = [c for c in display_cols if c in result_df.columns]
    result_view = result_df[existing_cols].copy()
    if "stage" in result_view.columns:
        result_view["stage_display"] = result_view["stage"].map(display_stage)
    st.dataframe(result_view, use_container_width=True)

    st.subheader(tr("monthly_cost_pivot"))
    pivot_df = monthly_cost_pivot(st.session_state.monthly_costs_df)
    st.dataframe(pivot_df, use_container_width=True)

with tab6:
    annual_metrics_df = summarize_monthly_metrics(st.session_state.monthly_metrics_df)
    annual_cost_df = summarize_monthly_costs(st.session_state.monthly_costs_df)
    result_df = merge_annual_data(preview_df, annual_metrics_df, annual_cost_df, edited_yield_targets, edited_weights, edited_cost_model)

    excel_bytes = to_excel_bytes(
        {
            "farm_master": preview_df,
            "monthly_metrics": st.session_state.monthly_metrics_df,
            "monthly_costs": st.session_state.monthly_costs_df,
            "cost_model": edited_cost_model,
            "stage_yield_targets": edited_yield_targets,
            "stage_weights": edited_weights,
            "annual_result": result_df,
            "monthly_cost_pivot": monthly_cost_pivot(st.session_state.monthly_costs_df),
        }
    )

    st.download_button(
        label=tr("download_excel"),
        data=excel_bytes,
        file_name="jatropha_farm_evaluation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.download_button(
        label=tr("download_metrics_csv"),
        data=df_to_csv_bytes(st.session_state.monthly_metrics_df),
        file_name="monthly_metrics.csv",
        mime="text/csv",
    )
    st.download_button(
        label=tr("download_costs_csv"),
        data=df_to_csv_bytes(st.session_state.monthly_costs_df),
        file_name="monthly_costs.csv",
        mime="text/csv",
    )
    st.download_button(
        label=tr("download_annual_csv"),
        data=df_to_csv_bytes(result_df),
        file_name="annual_result.csv",
        mime="text/csv",
    )
    st.info(tr("pdf_not_implemented"))

with st.expander(tr("recommended_csv")):
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

**monthly_metrics.csv**
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

**monthly_costs.csv**
- farm_id
- month
- cost_item
- amount_php
- notes

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
