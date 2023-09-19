import streamlit as st

from generate import generate_cover_letter


def check_linkedin_url(url: str) -> bool:
    return url.startswith(r"https://www.linkedin.com/jobs/view")


def check_openai_api_key(openai_api_key: str) -> bool:
    return openai_api_key.startswith("sk-")


if __name__ == "__main__":
    st.title("Cover Letter powered by AI")

    other_information_text = (
        "What do you think is the company culture?\n"
        "What makes you different? What's your motivations?\n"
        "Other informations relevant to the application?\n"
    )

    if "openai_api_key" not in st.session_state:
        st.session_state["openai_api_key"] = ""

    with st.form("generate"):
        st.session_state["openai_api_key"] = st.sidebar.text_input(
            "ChatGPT API Key *", value=st.session_state["openai_api_key"]
        )

        model = st.sidebar.radio(
            "Model:", ["gpt-3.5-turbo", "gpt-4"], horizontal=True
        )
        temperature = st.sidebar.slider("Temperature", 0.0, 1.0, value=0.7)
        linkedin_url = st.text_area("Linkedin Job URL: *")
        cv_file = st.file_uploader(
            "Upload Resume:", type=["pdf"], accept_multiple_files=False
        )
        other = st.text_area("Other informations:", other_information_text)
        language = st.radio(
            "Cover letter language:", ["French", "English"], horizontal=True
        )

        submit = st.form_submit_button("Generate")

    if (
        submit
        and check_linkedin_url(linkedin_url)
        and check_openai_api_key(st.session_state["openai_api_key"])
    ):
        with st.spinner("Thinking..."):
            data = {
                "url": linkedin_url,
                "cv": cv_file,
                "other": other,
            }
            model_parameters = {
                "api_key": st.session_state["openai_api_key"],
                "temperature": temperature,
                "model": model,
            }
            st.write(generate_cover_letter(data, model_parameters, language))

    else:
        st.warning("Please provide your API key and a Linkedin url", icon="⚠")
