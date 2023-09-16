import streamlit as st

from generate import generate_cover_letter

if __name__ == "__main__":
    st.title("Cover Letter powered by AI")

    if "openai_api_key" not in st.session_state:
        print("ok")
        st.session_state["openai_api_key"] = ""

    with st.form("generate"):
        st.session_state["openai_api_key"] = st.sidebar.text_input(
            "ChatGPT API Key *", value=st.session_state["openai_api_key"]
        )

        temperature = st.sidebar.slider("Temperature", 0.0, 1.0, value=0.3)
        linkedin_url = st.text_area("Linkedin Job URL: *")
        cv_file = st.file_uploader(
            "Upload CV", type=["pdf"], accept_multiple_files=False
        )
        other = st.text_area("Other informations:")

        submit = st.form_submit_button("Generate")

    if submit and linkedin_url and st.session_state["openai_api_key"]:
        with st.chat_message("ai"):
            with st.spinner("Thinking..."):
                data = {
                    "url": linkedin_url,
                    "cv": cv_file,
                    "other": other,
                }
                model_parameters = {
                    "api_key": st.session_state["openai_api_key"],
                    "temperature": temperature,
                }
                st.write(generate_cover_letter(data, model_parameters))

    else:
        st.warning("Please provide your API key and a Linkedin url", icon="⚠")
