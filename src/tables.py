import streamlit as st

def render_data_table(df_filtered):
    with st.expander("📄 Ver datos en tabla"):
        st.dataframe(
            df_filtered.sort_values(
                ["ticker", "date"],
                ascending=[True, False]
            ),
            use_container_width=True
        )
