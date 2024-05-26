import streamlit as st
import pandas as pd
import io

def obter_dados_paciente():
    st.subheader("Dados do Paciente 🩺")
    paciente = st.text_input("Paciente:")
    dia_da_semana = st.selectbox("Dia da Semana:", ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"])
    nome_da_dieta = st.text_input("Nome da Dieta:")
    leito = st.text_input("Leito:")
    data = st.date_input("Data:")
    return paciente, dia_da_semana, nome_da_dieta, leito, data

def mostrar_opcoes_ingesta(opcoes_ingesta, imagens_ingesta, refeicao):
    st.subheader(refeicao)
    selected_refeicao = st.radio(
        f"Selecione uma opção para {refeicao.lower()}:",
        options=opcoes_ingesta,
        index=0,
        key=f"selected_{refeicao.lower()}"
    )

    for i, opcao in enumerate(opcoes_ingesta):
        if selected_refeicao == opcao:
            st.image(imagens_ingesta[i], width=150)
        st.write("")

    return selected_refeicao

def obter_motivos(refeicao):
   
    motivos = [
        "Enjoo ou Vômito",
        "Falta de Apetite",
        "Não gostei da Comida",
        "Dificuldade para Mastigar e Engolir",
        "Gostei da Comida",
    ]
    return st.multiselect(f"Motivos ({refeicao}):", motivos, key=f"motivos_{refeicao.lower()}")

def salvar_resultados(paciente, dia_da_semana, nome_da_dieta, leito, data, selected_almoco, selected_jantar, motivos_almoco, motivos_jantar):
    data_dict = {
        "Paciente": [paciente],
        "Dia da Semana": [dia_da_semana],
        "Nome da Dieta": [nome_da_dieta],
        "Leito": [leito],
        "Data": [str(data)],  # Converter a data para string
        "Almoço": [selected_almoco],
        "Motivos no Almoço": [', '.join(motivos_almoco)],
        "Jantar": [selected_jantar],
        "Motivos no Jantar": [', '.join(motivos_jantar)]
    }
    df = pd.DataFrame(data_dict)
    return df

def main():
    st.set_page_config(page_title="Check list", page_icon="🏥", layout='wide',initial_sidebar_state="expanded")
    # Título do aplicativo
    st.header("🍽 Avaliação da Ingestão Oral", divider='rainbow')

    paciente, dia_da_semana, nome_da_dieta, leito, data = obter_dados_paciente()

    st.sidebar.header("Avaliação Pacientes clinicos",  divider='rainbow')
    st.sidebar.image("paciente.JPG", use_column_width=True)

    # Avaliação da ingesta
    st.markdown("<h2 style='font-size:20px;'>Clique na opção que mais se aproxima da satisfação da refeição:</h2>", unsafe_allow_html=True)
    st.header("",divider='rainbow')

    opcoes_ingesta = [
        "Tudo no almoço",
        "Mais que a metade no almoço",
        "Metade no almoço",
        "Menos que a metade no almoço",
        "Nada no almoço"
    ]

    opcoes_ingesta1 = [
        "Tudo no jantar",
        "Mais que a metade no jantar",
        "Metade no jantar",
        "Menos que a metade no jantar",
        "Nada no jantar"


    ]

    # Imagens correspondentes às opções
    imagens_ingesta = [
        "tudo.jpg",
        "mais_metade.jpg",
        "metade.jpg",
        "menos.jpg",
        "nada.jpg"
    ]

    selected_almoco = mostrar_opcoes_ingesta(opcoes_ingesta, imagens_ingesta, "Almoço")
    motivos_almoco = obter_motivos("Almoço")

    st.header("",divider='rainbow')

    selected_jantar = mostrar_opcoes_ingesta(opcoes_ingesta1, imagens_ingesta, "Jantar")
    motivos_jantar = obter_motivos("Jantar")

    # Botão para submissão
    if st.button("Submeter Avaliação"):
        st.success("Avaliação submetida com sucesso!")
        df = salvar_resultados(paciente, dia_da_semana, nome_da_dieta, leito, data, selected_almoco, selected_jantar, motivos_almoco, motivos_jantar)

        # Se existir a planilha anterior, leia ela
        try:
            existing_df = pd.read_excel("avaliacao_ingesta_oral.xlsx")
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass

        st.write("### Resumo da Avaliação")
        st.write(df)

        # Salvar os dados na planilha
        with pd.ExcelWriter("avaliacao_ingesta_oral.xlsx") as writer:
            df.to_excel(writer, index=False, sheet_name='Avaliação')

        # Botão para download do Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Avaliação')
        output.seek(0)
        
        st.download_button(
            label="Baixar Resultados em Excel",
            data=output,
            file_name="avaliacao_ingesta_oral.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
