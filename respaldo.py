    def connect_to_dropbox():
    """Conecta a Dropbox usando el token."""
    try:
        token = st.secrets["DROPBOX_ACCESS_TOKEN"]
    except (FileNotFoundError, KeyError):
        token = "sl.u.AF9bp8sTRhKtGdYoRQWM2k1Kpep1ZpE1_ZtLSnT-c0LN4iltoQxito5ujKrmsxS4-xBTa5x_S1zZaFQFVaX2EB-k5QnI6Xz58bgjIEpPQwsSWaA4OJjHj5H5EPTmcFijisDARfNTaPeitpqllaBjrOV48SzrGjAt6VdnrBHebSY8cKFO0jBEwVSa2vdxWiA28TNBUNFFASSbD_nJ-y72EhutfM1MN5-MFDsnYwWtJJFN1qPh_3Au4DQQ8TlhC3CjO8ZAlzN07OPDHTulv8miOlVJd9w9frLqN9ZrZMMryMb1S3XjdG8QdlpR3MGpJNd2XcNS0ZUVfR4l6rWTzBTM_vIrcTtEYoe_uEfhJzEQoXK2ojikkpEp5BfqrlaaKiKaOSvvHLZtUwH2sE6uTyxCiv9DOP-k1QnBBqNiiStH-TvlBZ2xwGbq-dZmBxbiQGsMrLc_fJI_pkO4h-vGA97fmBseC9qKqsRnyDl6F9N9D6nyxi-wgXVhZdSOswwWnxvZFPETf_mJb3lU0bnugxt1TdeYsIqcTNSiZaB83dTIF1AelJxUMUkAGSZjnMTycnu2Z0LbiGJZ7szLuXvLTGnJF30cFXLb7YRjfpw_Yq63zjIQxg9hVj2eYM0C2De4ui0JY_iQydvlur0JvGw8tGAjbOFqpz4uUkpmnqsvhU6D4B_XJn0EMiZkEApBDDLqahjnGdhZTqOwbM-AuINeYUjm9nCShOfGSIikV9S8Me2cJriIarKGuzA3y3K7hYuVSilK82OfHD-1YKWdpQ3MnIS21c7VT7776IQVGr4bQhEtDogbQMEhAeveO_oEGz7PUVm1xtsyEaWnGTUCo2XaKAPjpzO792l4Th5MN2vELSSXFsbhtVggaxOQuqZo2Au7epiMLLzZtA_U4ep4SpmRy88MHb4Y55Gm3BgtKjd3YocQxEAeYKcRTvSdfc6zPvuZ54f2cwC4rKvoQoNT-ZemIqEAVkrKXl5Ofd78oDfuATFXu-uyCM3s1MPtEe_0RCIi2rolxO9BsMPaqgK25azsu1tK5a4o_JtVAnYh_GidlycBwCDbUjkY0Uz5m09OPbm_PJaotkRD-twYiu6Lgfw7QWXvOqUKnDADNnla6qRenLUPR7GN7hnbkRH3wxmXAdjhzlY754jJXjjC8WKcJxLBZUPPgJN1g_T_d6fqifzhRgpBeXrMkJhQXADEsD0OsZbGCtdqWct8hoU5_eSorD0M-qWdMArUbqX5G1sW3K7-n1wx79_3gh3mmZcIB1hmo9asKLSy7eX5xBUyL1BOfB0MDrazHowkUhqTD9Z3-hdnIYxya9tNBwKMcGbMg670lPosLuT7HoIFMBhGAhEwhPMkIYLXF14FXnBsqObKELPkMyGtAmwQYCemEsGxJH9RbxMyzXf36hgaGcmlcqrVQL8OG-CdHWcZsX0YnPs8t9_tf3AjWKJimLXm3QFI5Junh9JJLKtcTcu9u3XUSwMzIqyWs7NnzpTqjw0dBXL1oEruoPHHj3f8dg"
    return dropbox.Dropbox(token)
#-----------------------------------------------------------

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd
import dropbox
import os
import pytz # <-- LIBRERÍA PARA ZONA HORARIA

# --- Importar credenciales (solo para entorno local) ---
try:
    from config import GOOGLE_CREDS, SPREADSHEET_ID, SHEET_TAB_NAME, DROPBOX_ACCESS_TOKEN
except ImportError:
    # No hacer nada si no existe, se asumirá que estamos en la nube
    pass

# --- FUNCIONES DE CONEXIÓN Y DATOS ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

@st.cache_resource
def connect_to_google_sheets():
    """
    Conecta a Google Sheets. Usa los secretos de Streamlit si está desplegado,
    de lo contrario, usa el archivo config.py local.
    """
    try:
        creds_dict = st.secrets["google_creds"]
        spreadsheet_id = st.secrets["SPREADSHEET_ID"]
        sheet_tab_name = st.secrets["SHEET_TAB_NAME"]
    except (FileNotFoundError, KeyError):
        creds_dict = GOOGLE_CREDS
        spreadsheet_id = SPREADSHEET_ID
        sheet_tab_name = SHEET_TAB_NAME
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client, spreadsheet_id, sheet_tab_name

@st.cache_resource
def connect_to_dropbox():
    """Conecta a Dropbox usando el token."""
    try:
        token = st.secrets["DROPBOX_ACCESS_TOKEN"]
    except (FileNotFoundError, KeyError):
        token = "sl.u.AF9UxBXmVo7iZoU2pYVrBxCSwOMdeD2Kf3Vzpdvf9Sv80nr8xXbEUtvwJfPuppa3x1VAal3ezUBktIf_Ig9aoAF-VDjVGwXcbQyX01n-CqAVumiFwN1E4i9LY0XX4RUaST8LF5kEj1An95_kHu6l3KNLy__PC7ILNa5Yl0-2maHo3iwy7XRDT4QoI7CvSr2mW7vz6XJc17KfA8L9n4fTgXjdKOkUyw7rSFCmDLWSd187Yu6l74Oqf2uckv--ov1lcNY9dfpNYC3-Ag7RezaHgH6PgiZhPgHVNcr3-0oL8T0KNm12g3G-gVDtudatTu78pUktdV_2KlMP4F4Y5fwLTLg6PISHgE4-FHpTe1A7kIxiM5rDHRt0WXwV9sOVNcrXYtTzvCBwiHTEJjS174u9g_1LaE_oa22M1RF5WEpXBi5Y3OlzNvlaOnMJwR9wUnyFi7Mzh8NGB__os1WprJD_NWoqVVwTDyZU_kOt4A8pJBpOLVf8qCjEt6fB8CWWJ0zFozKPn2v3bYuRdOcSMkxFIhb8llgjvkj-1nJgsO53ogW-pS_6yWT3fHshT59lb_GIfollSDgfdn1lLociEV8zG6i2fyLlRs9Bma-IH-qE-36jTKxVVNSLG-ik_6CznDbB9uE6HeaCwV5lPI8sEbU8jf-QKLomb1vMbHTa6mui2v5m1lUUncgblVrxNTJjHm_GyfJyt2ZWZ-X60hnaaUNTx8LlwkqUR6G2htPn7-XWVXzN3AoyoA_aGzVno2EX_vpWixLrGhti63YiEdveURKiz0sWKSDSAUlmNEiN6PYyuTAqBhbKITTBARz_75zxP93JkHCUuVECMcYvlq9WyoGlYWC1rxrjSG9HXCd3qeFF9BG2bktuzKsCvJq4gxMO-dnTXrsZ13rXm_su_QOZYSlj4QZgvHYDU1SQLhcOsnxN2_ZRCvI0JUTUQK4s8lG78_t95s12CJKOyQAkPa2CmYapSkClnryNBhQRNdcuuM5NC8TEg3hy6kpMY3l-DGC6tVoNK57mbASaCfEAd4UjfOskODb7Iih1pGLsLZAobeAjDWHwVUv2lVEnk2R8mm0M5S90gRTGX2DkXcPpebPinuSYUNtUpQHa2HGrrgmfpM3Bf-Xc304UadYpklyKuZZJFx6x7fXIFWaKzKA02vNwQhDk3Id3yiDEhvHFxNKyWyKYPIwOCB1BvCjZHZZn4nTjyo3mWdrG1-NbeuRM4kDoCN9aigPnUefCWv3krpZXJ5D2yESrxqLiQXxUSVaPbPBBL5hc-xYmt2qlOqkCZS_HzWUXW6i7h_8cnX_yDMZChCoufEz1pzkBmwDl89j2-_sdoTr8OUqcau7ETcC4Bok2qXIPqqKW8HQhFC1qbjQu37KGiFqueMeipMGYwYaQxXcDxIXysISqKZQQNVm03UW5idAc1WcB3p2x5Wvb_JxGjfYn4pXKbmH297rtr8VmYSMLD90-e_gbog_GXNDNMuOOp0VpLP3i9iy0LZ2nFenLVOrvEq6jkg"
        return dropbox.Dropbox(token)

@st.cache_data(ttl=60)
def get_client_data(_gsheet_client, spreadsheet_id):
    """Lee la hoja 'Clientes' y devuelve los datos como un DataFrame."""
    try:
        spreadsheet = _gsheet_client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet("Clientes")
        data = worksheet.get_all_records()
        if not data: return pd.DataFrame(columns=['Alias Cliente', 'Saldo USDT', 'Saldo MXN'])
            
        df = pd.DataFrame(data)
        df['Saldo USDT'] = df['Saldo USDT'].astype(str).str.replace(r'[$,]', '', regex=True)
        df['Saldo MXN'] = df['Saldo MXN'].astype(str).str.replace(r'[$,]', '', regex=True)
        df['Saldo USDT'] = pd.to_numeric(df['Saldo USDT'], errors='coerce').fillna(0)
        df['Saldo MXN'] = pd.to_numeric(df['Saldo MXN'], errors='coerce').fillna(0)
        return df
    except gspread.exceptions.WorksheetNotFound:
        st.error("Error: No se encontró la hoja 'Clientes' en tu Google Sheet.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"No se pudo cargar la lista de clientes: {e}")
        return pd.DataFrame()

def upload_to_dropbox(dbx_client, file_object, client_name):
    """Sube un archivo a Dropbox y devuelve el link para compartir."""
    try:
        mexico_tz = pytz.timezone("America/Mexico_City")
        timestamp = datetime.now(mexico_tz).strftime("%Y%m%d_%H%M%S")
        dropbox_path = f"/{client_name.replace(' ', '_')}/{timestamp}_{file_object.name}"
        
        dbx_client.files_upload(file_object.getvalue(), dropbox_path, mode=dropbox.files.WriteMode('overwrite'))
        
        try:
            links = dbx_client.sharing_list_shared_links(path=dropbox_path).links
            link = links[0].url if links else None
        except dropbox.exceptions.ApiError as err:
            if 'shared_link_already_exists' in str(err):
                links = dbx_client.sharing_list_shared_links(path=dropbox_path).links
                link = links[0].url if links else None
            else: raise

        if link is None:
            link_metadata = dbx_client.sharing_create_shared_link_with_settings(dropbox_path)
            link = link_metadata.url
        
        return link.replace("?dl=0", "?raw=1")
    except Exception as e:
        st.warning(f"No se pudo subir el archivo a Dropbox: {e}")
        return ""

def update_client_balance(_gsheet_client, spreadsheet_id, client_alias, new_usdt, new_mxn):
    """Encuentra un cliente en la hoja 'Clientes' y actualiza sus saldos."""
    try:
        spreadsheet = _gsheet_client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet("Clientes")
        cell = worksheet.find(client_alias, in_column=2)
        if cell is None:
            st.warning(f"No se pudo encontrar al cliente '{client_alias}' para actualizar su saldo.")
            return False

        headers = worksheet.row_values(1)
        usdt_col = headers.index("Saldo USDT") + 1
        mxn_col = headers.index("Saldo MXN") + 1
        
        worksheet.update_cell(cell.row, mxn_col, new_mxn)
        worksheet.update_cell(cell.row, usdt_col, new_usdt)
        return True
    except Exception as e:
        st.warning(f"Hubo un error al actualizar el saldo del cliente: {e}")
        return False

def get_next_folio_number(_gsheet_client, spreadsheet_id, sheet_tab_name):
    """
    Revisa el último registro en la hoja para determinar el siguiente número de folio.
    Se reinicia cada día.
    """
    try:
        spreadsheet = _gsheet_client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(sheet_tab_name)
        all_values = worksheet.get_all_values()
        
        if len(all_values) < 2: return 1

        last_row = all_values[-1]
        last_folio = last_row[0]
        
        parts = last_folio.split('-')
        last_folio_date_str = f"{parts[0]}-{parts[1]}-{parts[2]}"
        last_folio_num = int(parts[3])

        today_date_str = datetime.now(pytz.timezone("America/Mexico_City")).strftime("%y-%m-%d")

        if last_folio_date_str == today_date_str:
            return last_folio_num + 1
        else:
            return 1
    except (ValueError, IndexError):
        return 1
    except Exception:
        return 1

# --- FUNCIONES DE LA INTERFAZ ---

def create_calculation_row(row_index, precio_compra, precio_venta, mode_vende, mode_compra):
    div_height = 78 if row_index == 0 else 38
    col_vende, _, col_compra = st.columns([1, 0.2, 1])
    if row_index == 0:
        with col_vende: st.subheader("Cliente Vende / Yo Compro")
        with col_compra: st.subheader("Cliente Compra / Yo Vendo")
    with col_vende:
        label_vende = "Monto en USDT a Recibir" if mode_vende == "USDT -> Pesos" else "Monto en Pesos a Pagar"
        resultado_suffix_vende = "MXN" if mode_vende == "USDT -> Pesos" else "USDT"
        col_monto, col_resultado, col_uploader = st.columns([0.8, 0.8, 0.4])
        with col_monto:
            label_visibility = "visible" if row_index == 0 else "collapsed"
            input_vende = st.number_input(label_vende, min_value=0.0, format="%.2f", step=100.0, key=f"input_vende_{row_index}", label_visibility=label_visibility)
        with col_resultado:
            if mode_vende == "Pesos -> USDT":
                pesos_a_pagar = input_vende; usdt_a_recibir = (pesos_a_pagar / precio_compra) if precio_compra > 0 else 0.0
                resultado_vende = usdt_a_recibir
            else: 
                usdt_a_recibir = input_vende; pesos_a_pagar = usdt_a_recibir * precio_compra
                resultado_vende = pesos_a_pagar
            st.markdown(f"""<div style="display: flex; align-items: center; justify-content: start; height: {div_height}px;"><p style='font-size: 28px; font-weight: bold; color: #228B22; margin: 0;'>{resultado_vende:,.2f} {resultado_suffix_vende}</p></div>""", unsafe_allow_html=True)
        with col_uploader:
            st.file_uploader("Comprobante", type=["png", "jpg", "jpeg"], key=f"uploader_vende_{row_index}", label_visibility="collapsed")
    with col_compra:
        label_compra = "Monto en USDT a Entregar" if mode_compra == "USDT -> Pesos" else "Monto en Pesos a Cobrar"
        resultado_suffix_compra = "MXN" if mode_compra == "USDT -> Pesos" else "USDT"
        col_monto, col_resultado, col_uploader = st.columns([0.8, 0.8, 0.4])
        with col_monto:
            label_visibility = "visible" if row_index == 0 else "collapsed"
            input_compra = st.number_input(label_compra, min_value=0.0, format="%.2f", step=100.0, key=f"input_compra_{row_index}", label_visibility=label_visibility)
        with col_resultado:
            if mode_compra == "Pesos -> USDT":
                pesos_a_cobrar = input_compra; usdt_a_entregar = (pesos_a_cobrar / precio_venta) if precio_venta > 0 else 0.0
                resultado_compra = usdt_a_entregar
            else:
                usdt_a_entregar = input_compra; pesos_a_cobrar = usdt_a_entregar * precio_venta
                resultado_compra = pesos_a_cobrar
            st.markdown(f"""<div style="display: flex; align-items: center; justify-content: start; height: {div_height}px;"><p style='font-size: 28px; font-weight: bold; color: #DC143C; margin: 0;'>{resultado_compra:,.2f} {resultado_suffix_compra}</p></div>""", unsafe_allow_html=True)
        with col_uploader:
            st.file_uploader("Comprobante", type=["png", "jpg", "jpeg"], key=f"uploader_compra_{row_index}", label_visibility="collapsed")
    return {"pesos_pagar": pesos_a_pagar, "usdt_recibir": usdt_a_recibir, "pesos_cobrar": pesos_a_cobrar, "usdt_entregar": usdt_a_entregar}

def create_ajuste_row(row_index):
    col_pago, _, col_recibo = st.columns([1, 0.2, 1])
    if row_index == 0:
        with col_pago: st.subheader("Pagos (Salidas)")
        with col_recibo: st.subheader("Recibos (Entradas)")
    with col_pago:
        col_monto, col_uploader = st.columns([1, 0.4])
        with col_monto:
            pago_monto = st.number_input("Monto del Pago", min_value=0.0, format="%.2f", key=f"pago_monto_{row_index}", label_visibility="collapsed")
            pago_moneda = st.radio("Moneda del Pago", ["MXN", "USDT"], key=f"pago_moneda_{row_index}", horizontal=True, index=1)
        with col_uploader:
            st.file_uploader("Comprobante", type=["png", "jpg", "jpeg"], key=f"uploader_pago_{row_index}", label_visibility="collapsed")
    with col_recibo:
        col_monto, col_uploader = st.columns([1, 0.4])
        with col_monto:
            recibo_monto = st.number_input("Monto del Recibo", min_value=0.0, format="%.2f", key=f"recibo_monto_{row_index}", label_visibility="collapsed")
            recibo_moneda = st.radio("Moneda del Recibo", ["MXN", "USDT"], key=f"recibo_moneda_{row_index}", horizontal=True, index=1)
        with col_uploader:
            st.file_uploader("Comprobante", type=["png", "jpg", "jpeg"], key=f"uploader_recibo_{row_index}", label_visibility="collapsed")
    return {"pago_monto": pago_monto, "pago_moneda": pago_moneda, "recibo_monto": recibo_monto, "recibo_moneda": recibo_moneda}

def main():
    st.set_page_config(page_title="Calculadora y Registro", page_icon="🏦", layout="wide")
    st.markdown("""
    <style>
        [data-testid="stFileUploader"] section [data-testid="stFileUploaderDropzone"] {display: none;}
        [data-testid="stFileUploader"] section {padding: 0;border: none;}
        [data-testid="stFileUploader"] {padding-top: 28px;}
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Calculadora y Registro de Operaciones 🏦</h1>", unsafe_allow_html=True)
    st.markdown("---")
    gsheet_client, SPREADSHEET_ID, SHEET_TAB_NAME = connect_to_google_sheets()
    dbx_client = connect_to_dropbox()

    def add_calculo_row():
        if st.session_state.num_rows < 15: st.session_state.num_rows += 1
    def add_ajuste_row():
        st.session_state.num_ajustes += 1
    def limpiar_calculos_callback():
        for i in range(st.session_state.num_rows):
            if f"input_vende_{i}" in st.session_state: st.session_state[f"input_vende_{i}"] = 0.0
            if f"input_compra_{i}" in st.session_state: st.session_state[f"input_compra_{i}"] = 0.0
            if f"uploader_vende_{i}" in st.session_state: del st.session_state[f"uploader_vende_{i}"]
            if f"uploader_compra_{i}" in st.session_state: del st.session_state[f"uploader_compra_{i}"]
        st.session_state.num_rows = 1
    def limpiar_ajustes_callback():
        for i in range(st.session_state.num_ajustes):
            if f"pago_monto_{i}" in st.session_state: st.session_state[f"pago_monto_{i}"] = 0.0
            if f"recibo_monto_{i}" in st.session_state: st.session_state[f"recibo_monto_{i}"] = 0.0
            if f"uploader_pago_{i}" in st.session_state: del st.session_state[f"uploader_pago_{i}"]
            if f"uploader_recibo_{i}" in st.session_state: del st.session_state[f"uploader_recibo_{i}"]
        st.session_state.num_ajustes = 1
    def limpiar_todo_callback():
        limpiar_calculos_callback()
        limpiar_ajustes_callback()
        if "cliente_selector" in st.session_state: st.session_state.cliente_selector = "-- Seleccione un Cliente --"

    st.header("1. Configuración de Operación")
    col_cliente, col_compra, col_venta = st.columns(3)
    with col_cliente:
        st.subheader("Cliente y Balance")
        client_df = get_client_data(gsheet_client, SPREADSHEET_ID)
        balance_inicial_usdt, balance_inicial_pesos, selected_client_name = 0.0, 0.0, ""
        if not client_df.empty:
            client_list = ["-- Seleccione un Cliente --"] + client_df['Alias Cliente'].tolist()
            selected_client_name = st.selectbox("Cliente", client_list, key="cliente_selector")
            if selected_client_name != "-- Seleccione un Cliente --":
                client_data = client_df[client_df['Alias Cliente'] == selected_client_name].iloc[0]
                balance_inicial_usdt = float(client_data['Saldo USDT'])
                balance_inicial_pesos = float(client_data['Saldo MXN'])
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1: st.metric("Saldo USDT", f"{balance_inicial_usdt:,.2f}")
                with metric_col2: st.metric("Saldo Pesos", f"${balance_inicial_pesos:,.2f}")
                st.caption("Positivo = cliente te debe. Negativo = tú le debes.")
        else:
            st.warning("No se pudieron cargar los clientes.")
    with col_compra:
        st.subheader("Configuración de Compra")
        precio_compra_casa = st.number_input("Tasa de Compra", value=18.55, format="%.4f", key="precio_compra_input")
        mode_vende = st.radio("Modo para 'Cliente Vende / Yo Compro'", ("Pesos -> USDT", "USDT -> Pesos"), horizontal=True, key="mode_vende")
    with col_venta:
        st.subheader("Configuración de Venta")
        precio_venta_casa = st.number_input("Tasa de Venta", value=19.44, format="%.4f", key="precio_venta_input")
        mode_compra = st.radio("Modo para 'Cliente Compra / Yo Vendo'", ("Pesos -> USDT", "USDT -> Pesos"), horizontal=True, key="mode_compra")
    st.markdown("---")

    st.header("2. Operaciones de Compra/Venta")
    if 'num_rows' not in st.session_state: st.session_state.num_rows = 1
    col1, col2, _ = st.columns([1.3, 1.3, 5])
    with col1: st.button("➕ Añadir Cálculo", on_click=add_calculo_row, use_container_width=True)
    with col2: st.button("🔄 Limpiar Cálculos", use_container_width=True, on_click=limpiar_calculos_callback)
    st.markdown("<br>", unsafe_allow_html=True)
    all_rows_data = [create_calculation_row(i, precio_compra_casa, precio_venta_casa, mode_vende, mode_compra) for i in range(st.session_state.num_rows)]
    st.markdown("---")

    st.header("3. Pagos y Recibos (Ajustes de Caja)")
    if 'num_ajustes' not in st.session_state: st.session_state.num_ajustes = 1
    all_ajustes_data = [create_ajuste_row(i) for i in range(st.session_state.num_ajustes)]
    col_ajuste1, col_ajuste2, _ = st.columns([1.3, 1.3, 5])
    with col_ajuste1: st.button("➕ Añadir Ajuste", on_click=add_ajuste_row, use_container_width=True)
    with col_ajuste2: st.button("🔄 Limpiar Ajustes", use_container_width=True, on_click=limpiar_ajustes_callback)
    st.markdown("---")
    
    st.header("4. Totales y Balance Final")
    pagar_pesos_sum = sum(d['pesos_pagar'] for d in all_rows_data)
    recibir_usdt_sum = sum(d['usdt_recibir'] for d in all_rows_data)
    cobrar_pesos_sum = sum(d['pesos_cobrar'] for d in all_rows_data)
    entregar_usdt_sum = sum(d['usdt_entregar'] for d in all_rows_data)
    ajuste_neto_pesos = sum(d['pago_monto'] for d in all_ajustes_data if d['pago_moneda'] == 'MXN') - sum(d['recibo_monto'] for d in all_ajustes_data if d['recibo_moneda'] == 'MXN')
    ajuste_neto_usdt = sum(d['pago_monto'] for d in all_ajustes_data if d['pago_moneda'] == 'USDT') - sum(d['recibo_monto'] for d in all_ajustes_data if d['recibo_moneda'] == 'USDT')
    
    st.subheader("Totales Consolidados 🧮")
    total_recibidos_usdt_final = recibir_usdt_sum + (balance_inicial_usdt if balance_inicial_usdt > 0 else 0) + (ajuste_neto_usdt if ajuste_neto_usdt > 0 else 0)
    total_entregados_usdt_final = entregar_usdt_sum + (abs(balance_inicial_usdt) if balance_inicial_usdt < 0 else 0) + (abs(ajuste_neto_usdt) if ajuste_neto_usdt < 0 else 0)
    col_total_pagar, _, col_total_cobrar = st.columns([1, 0.2, 1])
    with col_total_pagar:
        st.metric(label="TOTAL PESOS PAGADOS (Operaciones)", value=f"${pagar_pesos_sum:,.2f}")
        st.metric(label="TOTAL USDT RECIBIDOS (Op. + Saldos)", value=f"{total_recibidos_usdt_final:,.2f} USDT")
    with col_total_cobrar:
        st.metric(label="TOTAL PESOS COBRADOS (Operaciones)", value=f"${cobrar_pesos_sum:,.2f}")
        st.metric(label="TOTAL USDT ENTREGADOS (Op. + Saldos)", value=f"{total_entregados_usdt_final:,.2f} USDT")
        
    st.subheader("Balance Final de Cierre ⚖️")
    balance_final_usdt = (recibir_usdt_sum + balance_inicial_usdt + ajuste_neto_usdt) - entregar_usdt_sum
    balance_final_pesos = 0 #(cobrar_pesos_sum + balance_inicial_pesos + ajuste_neto_pesos) - pagar_pesos_sum
    if balance_final_usdt > 0:
        status_texto = "TE DEBEN PAGAR (Utilidad en USDT)"
        status_color = "#228B22"
    elif balance_final_usdt < 0:
        status_texto = "DEBES PAGAR (Pérdida en USDT)"
        status_color = "#DC143C"
    else:
        status_texto = "BALANCE CERO"
        status_color = "gray"
    _, col_balance, _ = st.columns([1, 1.2, 1])
    with col_balance:
        st.metric(label="BALANCE FINAL USDT", value=f"{abs(balance_final_usdt):,.2f} USDT")
        st.markdown(f"<h3 style='text-align: center; color: {status_color};'>{status_texto}</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.header("5. Registrar Operaciones")
    col_save, col_clear_all = st.columns([3,1])
    with col_save:
        if st.button("💾 Guardar y Actualizar Saldo", use_container_width=True, type="primary"):
            if not selected_client_name or selected_client_name == "-- Seleccione un Cliente --":
                st.error("Por favor, seleccione un cliente antes de guardar.")
            else:
                operations_to_process = []
                for i, row_data in enumerate(all_rows_data):
                    if row_data["pesos_pagar"] > 0 or row_data["usdt_recibir"] > 0: operations_to_process.append({'type': 'Compra', 'index': i, 'data': row_data})
                    if row_data["pesos_cobrar"] > 0 or row_data["usdt_entregar"] > 0: operations_to_process.append({'type': 'Venta', 'index': i, 'data': row_data})
                for i, ajuste in enumerate(all_ajustes_data):
                    if ajuste['pago_monto'] > 0: operations_to_process.append({'type': 'Pago', 'index': i, 'data': ajuste})
                    if ajuste['recibo_monto'] > 0: operations_to_process.append({'type': 'Recibo', 'index': i, 'data': ajuste})

                if not operations_to_process:
                    st.warning("No hay operaciones con montos mayores a cero para guardar.")
                else:
                    progress_bar = st.progress(0, text="Iniciando guardado...")
                    
                    # --- LÓGICA DE FOLIO Y HORA DE MÉXICO ---
                    mexico_tz = pytz.timezone("America/Mexico_City")
                    now_mexico = datetime.now(mexico_tz)
                    timestamp = now_mexico.strftime("%Y-%m-%d %H:%M:%S")
                    today_prefix = now_mexico.strftime("%y-%m-%d")
                    next_folio_num = get_next_folio_number(gsheet_client, SPREADSHEET_ID, SHEET_TAB_NAME)
                    
                    data_to_save_batch = []
                    total_ops = len(operations_to_process)
                    
                    for i, op in enumerate(operations_to_process):
                        current_folio = f"{today_prefix}-{next_folio_num + i:04d}"
                        progress_text = f"Procesando operación {current_folio}..."
                        progress_bar.progress((i) / (total_ops + 2), text=progress_text)
                        link = ""
                        if op['type'] == 'Compra':
                            uploader_key = f"uploader_vende_{op['index']}"
                            if uploader_key in st.session_state and st.session_state[uploader_key]:
                                link = upload_to_dropbox(dbx_client, st.session_state[uploader_key], selected_client_name)
                            data_to_save_batch.append([current_folio, timestamp, selected_client_name, "Compra", op['data']["pesos_pagar"], op['data']["usdt_recibir"], precio_compra_casa, link])
                        elif op['type'] == 'Venta':
                            uploader_key = f"uploader_compra_{op['index']}"
                            if uploader_key in st.session_state and st.session_state[uploader_key]:
                                link = upload_to_dropbox(dbx_client, st.session_state[uploader_key], selected_client_name)
                            data_to_save_batch.append([current_folio, timestamp, selected_client_name, "Venta", op['data']["pesos_cobrar"], op['data']["usdt_entregar"], precio_venta_casa, link])
                        elif op['type'] == 'Pago':
                            uploader_key = f"uploader_pago_{op['index']}"
                            if uploader_key in st.session_state and st.session_state[uploader_key]:
                               link = upload_to_dropbox(dbx_client, st.session_state[uploader_key], selected_client_name)
                            pesos = op['data']['pago_monto'] if op['data']['pago_moneda'] == 'MXN' else ""
                            usdt = op['data']['pago_monto'] if op['data']['pago_moneda'] == 'USDT' else ""
                            data_to_save_batch.append([current_folio, timestamp, selected_client_name, "Pago", pesos, usdt, "N/A", link])
                        elif op['type'] == 'Recibo':
                            uploader_key = f"uploader_recibo_{op['index']}"
                            if uploader_key in st.session_state and st.session_state[uploader_key]:
                                link = upload_to_dropbox(dbx_client, st.session_state[uploader_key], selected_client_name)
                            pesos = op['data']['recibo_monto'] if op['data']['recibo_moneda'] == 'MXN' else ""
                            usdt = op['data']['recibo_monto'] if op['data']['recibo_moneda'] == 'USDT' else ""
                            data_to_save_batch.append([current_folio, timestamp, selected_client_name, "Recibo", pesos, usdt, "N/A", link])
                    
                    try:
                        progress_bar.progress((total_ops + 1) / (total_ops + 2), text="Guardando en Google Sheets...")
                        sheet = gsheet_client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_TAB_NAME)
                        sheet.append_rows(data_to_save_batch, value_input_option='USER_ENTERED')
                        
                        progress_bar.progress(1.0, text="Actualizando saldo del cliente...")
                        update_success = update_client_balance(gsheet_client, SPREADSHEET_ID, selected_client_name, balance_final_usdt, balance_final_pesos)
                        
                        progress_bar.empty()
                        if update_success:
                            st.success(f"✅ ¡Éxito! Se guardaron las operaciones y se actualizó el saldo.")
                        else:
                            st.success(f"✅ ¡Éxito! Se guardaron las operaciones.")
                        st.balloons()
                    except Exception as e:
                        progress_bar.empty()
                        st.error(f"❌ Error al guardar: {e}")
    with col_clear_all:
        st.button("🔄 Limpiar Todo", use_container_width=True, on_click=limpiar_todo_callback)

if __name__ == "__main__":
    main()