# Streamlit Cloud folder structure

Put these files in the same GitHub repo folder:

.
├── app.py
├── requirements.txt
├── farm_master.csv
├── monthly_input.csv
├── cost_model.csv
├── stage_yield_targets.csv
└── stage_weights.csv

## Deploy
1. Push this folder to GitHub.
2. In Streamlit Community Cloud, choose the repo.
3. Set `app.py` as the main file.
4. Deploy.

## Notes
- `app.py` should be the Streamlit app code already prepared in canvas.
- The CSV files are editable templates.
- You can later replace sample data with actual farm data.
