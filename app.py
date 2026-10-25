import streamlit as st

from editor_core import TwoStackEditor

st.set_page_config(page_title="StackWrite | Undo & Redo", page_icon="↶", layout="wide")

st.markdown(
    """
    <style>
      .stApp { background: #f7f8fc; color: #172033; }
      .hero { padding: 1.5rem 0 .7rem; }
      .eyebrow { color: #4f46e5; font-weight: 700; letter-spacing: .08em; font-size: .76rem; text-transform: uppercase; }
      .hero h1 { margin: .2rem 0; font-size: 2.3rem; letter-spacing: -.045em; }
      .hero p { margin: 0; color: #65708a; font-size: 1.03rem; }
      .metric-card { background: white; border: 1px solid #e8eaf2; border-radius: 14px; padding: 1rem 1.1rem; }
      .metric-label { color: #7b8499; font-size: .78rem; font-weight: 600; text-transform: uppercase; letter-spacing: .06em; }
      .metric-value { color: #1f2937; font-size: 1.55rem; font-weight: 750; margin-top: .15rem; }
      div.stButton > button { border-radius: 10px; font-weight: 650; min-height: 2.7rem; }
      div[data-testid="stTextArea"] textarea { border-radius: 14px; border: 1px solid #dde1ec; padding: 1rem; font-size: 1rem; line-height: 1.6; }
      .stack-title { font-weight: 750; font-size: 1.05rem; }
      .stack-note { color: #7b8499; font-size: .86rem; }
      .footer { color: #8b93a7; font-size: .83rem; padding: 1.5rem 0 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialise() -> None:
    if "engine" not in st.session_state:
        starter = "Welcome to StackWrite!\n\nType here to create your own history. Every edit is saved as a snapshot."
        st.session_state.engine = TwoStackEditor(starter)
        st.session_state.editor = starter


def save_edit() -> None:
    engine = st.session_state.engine
    if engine.edit(st.session_state.editor):
        st.toast("Edit saved to the Undo stack")


def do_undo() -> None:
    engine = st.session_state.engine
    if engine.undo():
        st.session_state.editor = engine.current_text
    else:
        st.toast("Nothing left to undo")


def do_redo() -> None:
    engine = st.session_state.engine
    if engine.redo():
        st.session_state.editor = engine.current_text
    else:
        st.toast("Nothing left to redo")


def reset_document() -> None:
    st.session_state.engine = TwoStackEditor("")
    st.session_state.editor = ""


def preview(text: str) -> str:
    cleaned = text.replace("\n", " ↵ ")
    return cleaned if len(cleaned) <= 56 else cleaned[:53] + "..."


initialise()
engine = st.session_state.engine

st.markdown("""<div class="hero"><div class="eyebrow">Data Structures Mini Project</div><h1>StackWrite</h1><p>A text editor history powered by two stacks - clear, fast, and easy to demonstrate.</p></div>""", unsafe_allow_html=True)

top1, top2, top3, top4 = st.columns(4)
with top1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Characters</div><div class="metric-value">{len(engine.current_text)}</div></div>', unsafe_allow_html=True)
with top2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Words</div><div class="metric-value">{len(engine.current_text.split())}</div></div>', unsafe_allow_html=True)
with top3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Undo states</div><div class="metric-value">{len(engine.undo_stack)}</div></div>', unsafe_allow_html=True)
with top4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Redo states</div><div class="metric-value">{len(engine.redo_stack)}</div></div>', unsafe_allow_html=True)

st.write("")
left, right = st.columns([1.75, 1], gap="large")
with left:
    st.subheader("Document")
    st.caption("Each time you change the text, the previous version moves onto the Undo stack.")
    st.text_area("Editor", key="editor", height=360, label_visibility="collapsed", on_change=save_edit, placeholder="Start writing...")
    action1, action2, action3, _ = st.columns([1, 1, 1, 1.5])
    with action1:
        st.button("↶  Undo", use_container_width=True, disabled=not engine.undo_stack, on_click=do_undo)
    with action2:
        st.button("↷  Redo", use_container_width=True, disabled=not engine.redo_stack, on_click=do_redo)
    with action3:
        st.button("New document", use_container_width=True, on_click=reset_document)

with right:
    st.markdown('<div class="stack-title">Live history</div><div class="stack-note">The top item is used first.</div>', unsafe_allow_html=True)
    with st.expander(f"Undo stack  •  {len(engine.undo_stack)} snapshots", expanded=True):
        if engine.undo_stack:
            for number, item in enumerate(reversed(engine.undo_stack), 1):
                st.code(f"TOP  {number}. {preview(item) or '[empty document]'}", language=None)
        else:
            st.info("No previous state yet.")
    with st.expander(f"Redo stack  •  {len(engine.redo_stack)} snapshots", expanded=True):
        if engine.redo_stack:
            for number, item in enumerate(reversed(engine.redo_stack), 1):
                st.code(f"TOP  {number}. {preview(item) or '[empty document]'}", language=None)
        else:
            st.info("Redo becomes available after an undo.")
    st.markdown("---")
    st.markdown("**Why two stacks?**  Undo removes the latest state with O(1) pop. Redo stores that removed state for an O(1) restore.")

st.markdown('<div class="footer">BUILD BY ABHI</div>', unsafe_allow_html=True)
