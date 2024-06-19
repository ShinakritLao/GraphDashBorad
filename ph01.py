import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data


@st.cache_data
def get_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source


st.sidebar.title("Dashboard")
page = st.sidebar.radio("Select Page", ["Page 1", "Page 2", "Page 3"])


if page == "Page 1":

    stock_data = get_data()

    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(stock_data, title="Graph 1")
        .mark_line()
        .encode(
            x="date",
            y="price",
            color="symbol",
        )
    )

    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(stock_data)
        .mark_rule()
        .encode(
            x="yearmonthdate(date)",
            y="price",
            opacity=alt.condition(hover, alt.value(0.5), alt.value(0)),
            tooltip=[
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("price", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )

    data_layer = lines + points + tooltips

    ANNOTATIONS = [
        ("Sep 01, 2007", 450, "🙂", "Something's going well for GOOG & AAPL."),
        ("Nov 01, 2008", 220, "🙂", "The market is recovering."),
        ("Dec 01, 2007", 750, "😱", "Something's going wrong for GOOG & AAPL."),
        ("Dec 01, 2009", 680, "😱", "A hiccup for GOOG."),
    ]
    annotations_df = pd.DataFrame(
        ANNOTATIONS, columns=["date", "price", "marker", "description"]
    )
    annotations_df.date = pd.to_datetime(annotations_df.date)

    annotation_layer = (
        alt.Chart(annotations_df)
        .mark_text(size=20, dx=-10, dy=0, align="left")
        .encode(x="date:T", y=alt.Y("price:Q"), text="marker", tooltip="description")
    )

    combined_chart = data_layer

    st.markdown(
        """
        <style>
        .top-row .element-container {
            padding-right: 50% !important;
        }
        .bottom-row .element-container {
            padding-right: 50% !important;
        }
        .row-separator {
            margin-bottom: 50px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    st.markdown('<div class="row-separator"></div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col1:
        st.markdown('<div class="top-row"></div>', unsafe_allow_html=True)
        st.altair_chart(combined_chart, use_container_width=True)

    with col2:
        st.markdown('<div class="top-row"></div>', unsafe_allow_html=True)
        st.altair_chart(combined_chart, use_container_width=True)

    with col3:
        st.markdown('<div class="bottom-row"></div>', unsafe_allow_html=True)
        st.altair_chart(combined_chart, use_container_width=True)

    with col4:
        st.markdown('<div class="bottom-row"></div>', unsafe_allow_html=True)
        st.altair_chart(combined_chart, use_container_width=True)


elif page == "Page 2":

    stock_data = get_data()

    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(stock_data, title="Evolution of stock prices")
        .mark_line()
        .encode(
            x="date",
            y="price",
            color="symbol",
        )
    )

    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(stock_data)
        .mark_rule()
        .encode(
            x="yearmonthdate(date)",
            y="price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("price", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )

    data_layer = lines + points + tooltips

    ANNOTATIONS = [
        ("Sep 01, 2007", 450, "🙂", "Something's going well for GOOG & AAPL."),
        ("Nov 01, 2008", 220, "🙂", "The market is recovering."),
        ("Dec 01, 2007", 750, "😱", "Something's going wrong for GOOG & AAPL."),
        ("Dec 01, 2009", 680, "😱", "A hiccup for GOOG."),
    ]
    annotations_df = pd.DataFrame(
        ANNOTATIONS, columns=["date", "price", "marker", "description"]
    )
    annotations_df.date = pd.to_datetime(annotations_df.date)

    annotation_layer = (
        alt.Chart(annotations_df)
        .mark_text(size=20, dx=-10, dy=0, align="left")
        .encode(x="date:T", y=alt.Y("price:Q"), text="marker", tooltip="description")
    )

    combined_chart = data_layer + annotation_layer
    st.altair_chart(combined_chart, use_container_width=True)


elif page == "Page 3":

    stock_data = get_data()

    stock_chart_data = stock_data.groupby('symbol')['price'].mean().reset_index()

    hover = alt.selection_single(
        fields=["symbol"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    pie_chart = (
        alt.Chart(stock_chart_data)
        .mark_arc()
        .encode(
            theta=alt.Theta(field="price", type="quantitative"),
            color=alt.Color(field="symbol", type="nominal"),
            tooltip=['symbol', 'price'],
        )
        #.add_selection(hover)
    )

    pie_points = (
        alt.Chart(stock_chart_data)
        .mark_point(size=100, filled=True)
        .encode(
            theta=alt.Theta(field="price", type="quantitative"),
            color=alt.Color(field="symbol", type="nominal"),
            opacity=alt.condition(hover, alt.value(1), alt.value(0)),
        )
        .transform_filter(hover)
    )

    pie_tooltips = (
        alt.Chart(stock_chart_data)
        .mark_text(dx=15, dy=-15, fontSize=15, fontWeight="bold")
        .encode(
            theta=alt.Theta(field="price", type="quantitative"),
            color=alt.Color(field="symbol", type="nominal"),
            text=alt.condition(hover, "symbol:N", alt.value("")),
            tooltip=['symbol', 'price']
        )
        .transform_filter(hover)
    )

    pie_combined = pie_chart# + pie_points + pie_tooltips

    bar_chart = (
        alt.Chart(stock_chart_data)
        .mark_bar()
        .encode(
            x=alt.X("symbol", sort='-y'),
            y="price",
            color="symbol",
            tooltip=['symbol', 'price']
        )
        .add_selection(hover)
    )

    bar_points = (
        alt.Chart(stock_chart_data)
        .mark_circle(size=65)
        .encode(
            x=alt.X("symbol", sort='-y'),
            y="price",
            color="symbol",
            opacity=alt.condition(hover, alt.value(1), alt.value(0))
        )
        .transform_filter(hover)
    )

    bar_tooltips = (
        alt.Chart(stock_chart_data)
        .mark_rule()
        .encode(
            x=alt.X("symbol", sort='-y'),
            y="price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("symbol", title="Symbol"),
                alt.Tooltip("price", title="Price (USD)"),
            ]
        )
        .transform_filter(hover)
    )

    bar_combined = bar_chart + bar_points + bar_tooltips

    st.markdown(
        """
        <style>
        .top-row .element-container {
            padding-right: 50% !important;
        }
        .bottom-row .element-container {
            padding-right: 50% !important;
        }
        .row-separator {
            margin-bottom: 50px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .row-container {
            display: flex;
            flex-direction: column;
        }
        .chart-container {
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="row-container">', unsafe_allow_html=True)

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.altair_chart(pie_combined, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.altair_chart(bar_combined, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)