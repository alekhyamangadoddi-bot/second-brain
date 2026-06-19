import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Second Brain", layout="wide")

# -----------------------------
# SESSION STATE (PAGE CONTROL)
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# -----------------------------
# HEADER (HOME STYLE UI)
# -----------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>
        🧠 Second Brain
    </h1>
    <h4 style='text-align: center; color: gray;'>
        All your thoughts in one place
    </h4>
    """,
    unsafe_allow_html=True
)

# Brain Image
st.image(
    "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
    width=150
)

st.divider()

# -----------------------------
# MENU BUTTONS (APP HOME)
# -----------------------------
st.markdown("## Choose an option 👇")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Add Note"):
        st.session_state.page = "add"

with col2:
    if st.button("📄 View Notes"):
        st.session_state.page = "view"

with col3:
    if st.button("🔍 Search Notes"):
        st.session_state.page = "search"

st.divider()

# -----------------------------
# ADD NOTE PAGE
# -----------------------------
if st.session_state.page == "add":

    st.header("➕ Add New Note")

    title = st.text_input("Title")
    content = st.text_area("Content")

    if st.button("Save Note"):

        response = requests.post(
            f"{BACKEND_URL}/add-note",
            json={"title": title, "content": content}
        )

        if response.status_code == 200:
            st.success("Note saved successfully")
            st.rerun()

# -----------------------------
# VIEW NOTES PAGE
# -----------------------------
elif st.session_state.page == "view":

    st.header("📄 Your Notes")

    response = requests.get(f"{BACKEND_URL}/notes")
    notes = response.json()

    for note in notes:

        with st.container():
            st.subheader(note["title"])
            st.write(note["content"])

            if st.button(f"🗑️ Delete {note['title']}"):
                requests.delete(
                    f"{BACKEND_URL}/delete-note/{note['title']}"
                )
                st.success("Deleted!")
                st.rerun()

            st.divider()

# -----------------------------
# SEARCH PAGE
# -----------------------------
elif st.session_state.page == "search":

    st.header("🔍 Search Notes")

    keyword = st.text_input("Enter keyword")

    if keyword:

        response = requests.get(
            f"{BACKEND_URL}/search",
            params={"keyword": keyword}
        )

        notes = response.json()

        for note in notes:
            st.subheader(note["title"])
            st.write(note["content"])
            st.divider()