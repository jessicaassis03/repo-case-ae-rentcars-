-- Datasets carregados e limpos , validações de negócio , reservas: dropoff_date >= pick-up_date, consolidação de dicionário é essencial
import pandas as pd

# Função de limpeza genérica
def clean_dataframe(df, categorical_cols=None, unique_col=None):
    # Remove duplicatas
    if unique_col:
        df = df.drop_duplicates(subset=[unique_col])
    else:
        df = df.drop_duplicates()
    
    # Normaliza colunas categóricas
    if categorical_cols:
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower().str.strip()
    return df

# Carregar datasets
import pandas as pd

base_path = "C:/Case_Engineer/case_engineer_rencars/"

df_cancellations = pd.read_csv(base_path + "raw_cancellations.csv")
df_partners = pd.read_csv(base_path + "raw_partners.csv")
df_sessions = pd.read_csv(base_path + "raw_sessions.csv")
df_searches = pd.read_csv(base_path + "raw_searches.csv")
df_bookings = pd.read_csv(base_path + "raw_bookings.csv")
# Limpeza básica
df_partners = clean_dataframe(df_partners, categorical_cols=["status","tier"], unique_col="partner_id")
df_sessions = clean_dataframe(df_sessions, categorical_cols=["device","country"], unique_col="session_id")
df_searches = clean_dataframe(df_searches, categorical_cols=["pickup_location","dropoff_location"], unique_col="search_id")
df_bookings = clean_dataframe(df_bookings, categorical_cols=["status","pickup_location"], unique_col="booking_id")
df_cancellations = clean_dataframe(df_cancellations, categorical_cols=["reason","refund_status"], unique_col="cancellation_id")

# Validações de negócio
# Reservas: total_amount > 0 para confirmadas/concluídas
df_bookings = df_bookings[
    ~((df_bookings["status"].isin(["confirmed","completed"])) & (df_bookings["total_amount"] <= 0))
]

# Reservas: dropoff_date >= pickup_date
df_bookings = df_bookings[
    (pd.to_datetime(df_bookings["dropoff_date"]) >= pd.to_datetime(df_bookings["pickup_date"]))
]

# Buscas: dropoff_date >= pickup_date
df_searches = df_searches[
    (pd.to_datetime(df_searches["dropoff_date"]) >= pd.to_datetime(df_searches["pickup_date"]))
]

# Cancelamentos: refund_amount <= total_amount
df_cancellations = df_cancellations.merge(
    df_bookings[["booking_id","total_amount"]],
    on="booking_id",
    how="left"
)
df_cancellations = df_cancellations[
    (df_cancellations["refund_amount"].isna()) | 
    (df_cancellations["refund_amount"] <= df_cancellations["total_amount"])
]

# Consolidar em dicionário
dataframes = {
    "partners": df_partners,
    "sessions": df_sessions,
    "searches": df_searches,
    "bookings": df_bookings,
    "cancellations": df_cancellations
}

print("Datasets carregados e limpos:")
for name, df in dataframes.items():
    print(f"{name}: {len(df)} linhas")

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

