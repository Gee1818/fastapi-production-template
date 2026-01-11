from collections.abc import Sequence

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .health import health_page
from .test import test_page
from .training import training_page

PAGES: Sequence[StreamlitPage] = (  # noqa: RUF067
    st.Page(health_page, title="Health Page", icon=":material/favorite:"),
    st.Page(test_page, title="Test Page", icon=":material/check_circle:"),
    st.Page(training_page, title="Training Page", icon=":material/school:"),
)

__all__ = ["PAGES"]
