-- Datasets validações de regras de negócio, dados limpos e carregados , consolidação do dicionário e gráficos da receita ao longo do tempo, funil de conversão e conversão por País e Device
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




import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================
# 📁 PATHS
# =========================

BASE_PATH = "C:/Case_Engineer/case_engineer_rencars/"
PROCESSED_PATH = "data/processed/"

Path(PROCESSED_PATH).mkdir(parents=True, exist_ok=True)

# =========================
# 🧼 FUNÇÃO DE LIMPEZA
# =========================

def clean_dataframe(df, categorical_cols=None, unique_col=None):
    df = df.copy()

    if unique_col:
        df = df.drop_duplicates(subset=[unique_col])
    else:
        df = df.drop_duplicates()

    if categorical_cols:
        for col in categorical_cols:
            if col in df.columns:
                df.loc[:, col] = df[col].astype(str).str.lower().str.strip()

    return df

# =========================
# 📥 LOAD RAW
# =========================

df_cancellations = pd.read_csv(BASE_PATH + "raw_cancellations.csv")
df_partners = pd.read_csv(BASE_PATH + "raw_partners.csv")
df_sessions = pd.read_csv(BASE_PATH + "raw_sessions.csv")
df_searches = pd.read_csv(BASE_PATH + "raw_searches.csv")
df_bookings = pd.read_csv(BASE_PATH + "raw_bookings.csv")

# =========================
# 🧼 CLEAN
# =========================

df_partners = clean_dataframe(df_partners, ["status","tier"], "partner_id")
df_sessions = clean_dataframe(df_sessions, ["device","country"], "session_id")
df_searches = clean_dataframe(df_searches, ["pickup_location","dropoff_location"], "search_id")
df_bookings = clean_dataframe(df_bookings, ["status","pickup_location"], "booking_id")
df_cancellations = clean_dataframe(df_cancellations, ["reason","refund_status"], "cancellation_id")

# =========================
# 🔍 REGRAS DE NEGÓCIO
# =========================

df_bookings = df_bookings[
    ~((df_bookings["status"].isin(["confirmed","completed"])) & (df_bookings["total_amount"] <= 0))
].copy()

df_bookings = df_bookings[
    (pd.to_datetime(df_bookings["dropoff_date"]) >= pd.to_datetime(df_bookings["pickup_date"]))
].copy()

df_searches = df_searches[
    (pd.to_datetime(df_searches["dropoff_date"]) >= pd.to_datetime(df_searches["pickup_date"]))
].copy()

df_cancellations = df_cancellations.merge(
    df_bookings[["booking_id","total_amount"]],
    on="booking_id",
    how="left"
)

df_cancellations = df_cancellations[
    (df_cancellations["refund_amount"].isna()) |
    (df_cancellations["refund_amount"] <= df_cancellations["total_amount"])
].copy()

# =========================
# 💾 SALVAR DADOS LIMPOS
# =========================

df_bookings.to_csv(PROCESSED_PATH + "bookings_clean.csv", index=False)
df_sessions.to_csv(PROCESSED_PATH + "sessions_clean.csv", index=False)
df_searches.to_csv(PROCESSED_PATH + "searches_clean.csv", index=False)
df_cancellations.to_csv(PROCESSED_PATH + "cancellations_clean.csv", index=False)

print("✅ Dados processados salvos!")

# =========================
# 📊 DASHBOARD
# =========================
df_bookings["booking_date"] = pd.to_datetime(df_bookings["booked_at"]).dt.date

# 📈 Receita
revenue = df_bookings.groupby("booking_date")["total_amount"].sum().reset_index()

fig1 = px.line(revenue, x="booking_date", y="total_amount",
               title="Receita ao longo do tempo")
fig1.show()

# 🔻 Funil
funnel = pd.DataFrame({
    "stage": ["Sessions", "Searches", "Bookings"],
    "count": [
        df_sessions["session_id"].nunique(),
        df_searches["search_id"].nunique(),
        df_bookings["booking_id"].nunique()
    ]
})

fig2 = px.funnel(funnel, x="count", y="stage",
                 title="Funil de Conversão")
fig2.show()

# 🌍 Conversão por país/device
df = df_sessions.merge(df_searches, on="session_id", how="left") \
                .merge(df_bookings, on="session_id", how="left")

seg = df.groupby(["country", "device"]).agg({
    "session_id": "nunique",
    "booking_id": "nunique"
}).reset_index()

seg["conversion_rate"] = seg["booking_id"] / seg["session_id"]

fig3 = px.bar(seg, x="country", y="conversion_rate",
              color="device",
              title="Conversão por País e Device")
fig3.show()

# ❌ Cancelamentos
cancel = df_cancellations.groupby("partner_id").size().reset_index(name="cancellations")

fig4 = px.bar(cancel.sort_values("cancellations", ascending=False).head(10),
              x="partner_id", y="cancellations",
              title="Top 10 Cancelamentos")
fig4.show()

# 🏆 Receita por parceiro
top = df_bookings.groupby("partner_id")["total_amount"].sum().reset_index()

fig5 = px.bar(top.sort_values("total_amount", ascending=False).head(10),
              x="partner_id", y="total_amount",
              title="Top 10 Parceiros por Receita")
fig5.show()


