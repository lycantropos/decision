from itertools import repeat

from hypothesis import strategies as st

MAX_AMOUNT = 10**4
amounts = st.integers(0, MAX_AMOUNT)
denominations = st.integers(1, MAX_AMOUNT)
denominations_lists = st.lists(denominations, min_size=1, unique=True)
invalid_amounts = st.integers(max_value=-1)
invalid_denominations_lists: st.SearchStrategy[list[int]] = st.lists(
    st.integers(max_value=0), unique=True
) | st.builds(list, st.builds(repeat, denominations, st.integers(2, 100)))
