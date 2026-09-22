import pandas as pd
import streamlit as st
import altair as alt


# ========================================================
# SHARED HELPERS (MATCHING LANDING PAGE)
# ========================================================

CATEGORY_COLORS = {
    "Food": "#E2914F",
    "Shopping": "#EC80A2",
    "Transport": "#6C9DE8",
    "Entertainment": "#4FC9B8",
    "Education": "#B48AF0",
    "Health": "#CF564A",
    "Utilities": "#D9A441",
    "Other": "#8B8A7C",
}


def render_colored_bars(series):
    """Renders horizontal progress bars for category breakdowns."""
    series = series.sort_values(ascending=False)
    total = float(series.sum())

    for label, amount in series.items():
        amount = float(amount)
        percentage = (amount / total * 100) if total > 0 else 0.0
        bar_color = CATEGORY_COLORS.get(str(label).strip(), "#8B8A7C")

        st.markdown(
            f'''
            <div style="margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-family: 'Inter', sans-serif;">
                    <span style="color: #9F9F9C; font-size: 12px; font-weight: 500;">{label}</span>
                    <span style="color: #696965; font-size: 11px; font-weight: 500;">{percentage:.1f}%</span>
                </div>
                <div style="width: 100%; height: 8px; background: #303030; border-radius: 4px; overflow: hidden;">
                    <div style="width: {percentage:.2f}%; height: 100%; background: {bar_color}; border-radius: 4px; transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);"></div>
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )


def render_altair_vertical_bar(df, x_col, y_col, height=280):
    """Renders vertical bar charts styled to match the landing page."""
    chart = alt.Chart(df).mark_bar(
        color='#5C8DFF',
        cornerRadiusTopLeft=2,
        cornerRadiusTopRight=2,
        cornerRadiusBottomLeft=0,
        cornerRadiusBottomRight=0
    ).encode(
        x=alt.X(f'{x_col}:N', 
                axis=alt.Axis(
                    labelColor='#9F9F9C', 
                    title=None, 
                    labelFontSize=11,
                    domain=False,
                    tickColor='#303030'
                ),
                sort=None),
        y=alt.Y(f'{y_col}:Q', 
                axis=alt.Axis(
                    labelColor='#9F9F9C', 
                    title=None, 
                    gridColor='#303030', 
                    labelFontSize=11,
                    domain=False,
                    tickCount=5
                ))
    ).properties(
        height=height,
        background='#1B1B1B',
        padding={"left": 10, "right": 20, "top": 20, "bottom": 10}
    ).configure_view(
        strokeWidth=0
    )
    st.altair_chart(chart, use_container_width=True)


def render_altair_line_chart(df, x_col, y_col, height=300):
    """Renders line charts styled to match the landing page."""
    line = alt.Chart(df).mark_line(
        color='#5C8DFF',
        strokeWidth=3,
        interpolate='monotone'
    ).encode(
        x=alt.X(f'{x_col}:N', 
                axis=alt.Axis(
                    labelColor='#9F9F9C', 
                    title=None, 
                    labelFontSize=11,
                    domain=False,
                    tickColor='#303030'
                ),
                sort=None),
        y=alt.Y(f'{y_col}:Q', 
                axis=alt.Axis(
                    labelColor='#9F9F9C', 
                    title=None, 
                    gridColor='#303030', 
                    labelFontSize=11,
                    domain=False,
                    tickCount=5
                ))
    )
    
    points = alt.Chart(df).mark_circle(
        color='#5C8DFF',
        size=60
    ).encode(
        x=f'{x_col}:N',
        y=f'{y_col}:Q'
    )
    
    chart = (line + points).properties(
        height=height,
        background='#1B1B1B',
        padding={"left": 10, "right": 20, "top": 20, "bottom": 10}
    ).configure_view(
        strokeWidth=0
    )
    
    st.altair_chart(chart, use_container_width=True)


def show_analytics(get_expenses, get_monthly_analytics, get_weekly_analytics, get_monthly_trend, get_monthly_comparison):

        # ========================================================
        # HEADER
        # ========================================================

        st.markdown(
            '<div class="section-label">'
            'Spending Analytics {Present to whole year}'
            '</div>',
            unsafe_allow_html=True
        )

        # ========================================================
        # LOAD DATA ONCE
        # ========================================================

        expenses = get_expenses()

        if expenses is None:
            st.error("Unable to retrieve expense data.")
            return

        expenses = expenses.copy()

        # ====================================================
        # PREPARE DATA
        # ====================================================

        if not expenses.empty:
            expenses["amount"] = pd.to_numeric(
                expenses["amount"], errors="coerce"
            ).fillna(0)

            expenses["created_at"] = pd.to_datetime(
                expenses["created_at"], errors="coerce", utc=True
            ).dt.tz_convert("Asia/Kathmandu")

            expenses["is_essential"] = (
                expenses["is_essential"].fillna(False).astype(bool)
                if "is_essential" in expenses.columns else False
            )
        else:
            expenses["amount"] = pd.Series(dtype="float64")
            expenses["created_at"] = pd.Series(dtype="datetime64[ns, Asia/Kathmandu]")

        # ====================================================
        # CURRENT TIME
        # ====================================================

        now = pd.Timestamp.now(tz="Asia/Kathmandu")
        today = now.normalize()
        month_start = pd.Timestamp(year=today.year, month=today.month, day=1, tz="Asia/Kathmandu")
        year_start = pd.Timestamp(year=today.year, month=1, day=1, tz="Asia/Kathmandu")

        def money(value):
            return "Rs. " + "{:,.2f}".format(float(value))

        # ====================================================
        # TODAY
        # ====================================================

        st.markdown('<div class="section-label">Today</div>', unsafe_allow_html=True)
        st.caption("Spending and transactions.")

        today_data = expenses[expenses["created_at"] >= today].copy() if not expenses.empty else expenses.copy()
        today_total = float(today_data["amount"].sum())
        today_count = len(today_data)

        today_col1, today_col2 = st.columns(2, gap="medium")
        with today_col1: st.metric("Spent Today", money(today_total))
        with today_col2: st.metric("Transactions", str(today_count))

        if today_count > 0:
            today_categories = today_data.groupby("category")["amount"].sum().sort_values(ascending=False)
            top_today_category = today_categories.index[0]
            top_today_amount = float(today_categories.iloc[0])

            st.caption("Most spent on " + str(top_today_category) + " · " + money(top_today_amount))

            today_highest = today_data.loc[today_data["amount"].idxmax()]
            st.caption("Biggest transaction: " + str(today_highest["description"]) + " · " + money(today_highest["amount"]))

            today_display = today_data[["description", "amount", "category", "is_essential"]].copy()
            today_display = today_display.rename(columns={"description": "Transaction", "amount": "Amount (Rs.)", "category": "Category", "is_essential": "Type"})
            today_display["Type"] = today_display["Type"].apply(lambda value: "Essential" if bool(value) else "Regular")
            today_display["Amount (Rs.)"] = today_display["Amount (Rs.)"].round(2)

            st.dataframe(today_display, use_container_width=True, hide_index=True)
        else:
            st.info("No expenses recorded today.")

        st.divider()

        # ====================================================
        # ESSENTIAL / UNEXPECTED SPENDING
        # ====================================================

        st.markdown('<div class="section-label">Essential & Unexpected</div>', unsafe_allow_html=True)
        st.caption("Important spending is separated from regular spending.")

        month_data = expenses[expenses["created_at"] >= month_start].copy()
        month_essential = month_data[month_data["is_essential"]].copy()
        month_regular = month_data[~month_data["is_essential"]].copy()

        essential_col1, essential_col2, essential_col3 = st.columns(3, gap="medium")
        with essential_col1: st.metric("Regular Spending", money(month_regular["amount"].sum()))
        with essential_col2: st.metric("Essential / Unexpected", money(month_essential["amount"].sum()))
        with essential_col3:
            total_month = float(month_data["amount"].sum())
            essential_share = (float(month_essential["amount"].sum()) / total_month * 100) if total_month > 0 else 0
            st.metric("Essential Share", "{:.1f}%".format(essential_share))

        if not month_essential.empty:
            essential_display = month_essential[["description", "amount", "category"]].rename(columns={"description": "Expense", "amount": "Amount (Rs.)", "category": "Category"})
            essential_display["Amount (Rs.)"] = essential_display["Amount (Rs.)"].round(2)
            st.dataframe(essential_display.head(8), use_container_width=True, hide_index=True)
        else:
            st.info("No essential or unexpected spending recorded this month.")

        st.divider()

        # ====================================================
        # THIS WEEK
        # ====================================================

        st.markdown('<div class="section-label">This Week</div>', unsafe_allow_html=True)
        st.caption("See how your spending is moving from Sunday to Saturday.")

        weekly = get_weekly_analytics()

        if weekly is None:
            st.warning("Weekly analytics are currently unavailable.")
        else:
            weekly_total = float(weekly.get("total_spending", 0))
            weekly_count = int(weekly.get("total_expenses", 0))
            weekly_average = float(weekly.get("average_expense", 0))

            week_col1, week_col2, week_col3 = st.columns(3, gap="medium")
            with week_col1: st.metric("Spent This Week", money(weekly_total))
            with week_col2: st.metric("Transactions", str(weekly_count))
            with week_col3: st.metric("Average", money(weekly_average))

            weekly_daily = pd.DataFrame(weekly.get("daily_spending", []))

            if not weekly_daily.empty:
                weekly_daily["date"] = pd.to_datetime(weekly_daily["date"], errors="coerce")
                weekly_daily["amount"] = pd.to_numeric(weekly_daily["amount"], errors="coerce").fillna(0)
                weekly_daily["Day"] = weekly_daily["date"].dt.strftime("%a")
                
                day_order = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
                weekly_daily["Day"] = pd.Categorical(weekly_daily["Day"], categories=day_order, ordered=True)
                weekly_daily = weekly_daily.sort_values("Day")

                # VERTICAL BAR CHART (Styled with Altair)
                daily_chart_df = weekly_daily[["Day", "amount"]].copy()
                render_altair_vertical_bar(daily_chart_df, "Day", "amount", 280)
                st.caption("Each bar shows how much you spent on that day.")

            weekly_categories = weekly.get("categories", {})
            if weekly_categories:
                weekly_category_series = pd.Series(weekly_categories, dtype="float64").sort_values(ascending=True)
                
                st.markdown('<div class="section-label">This Week by Category</div>', unsafe_allow_html=True)
                
                # HORIZONTAL PROGRESS BARS
                render_colored_bars(weekly_category_series)
                
                top_week_category = weekly_category_series.idxmax()
                st.caption("Most spent on " + str(top_week_category) + " this week.")

        st.divider()

        # ====================================================
        # THIS MONTH
        # ====================================================

        st.markdown('<div class="section-label">This Month</div>', unsafe_allow_html=True)
        st.caption("Understand where this month's money is going.")

        monthly = get_monthly_analytics(int(now.year), int(now.month))
        comparison = get_monthly_comparison(int(now.year), int(now.month))

        if monthly is None:
            st.warning("Monthly analytics are currently unavailable.")
        else:
            month_total = float(monthly.get("total_spending", 0))
            month_count = int(monthly.get("total_expenses", 0))
            month_average = float(monthly.get("average_expense", 0))

            month_col1, month_col2, month_col3 = st.columns(3, gap="medium")
            with month_col1: st.metric("Spent This Month", money(month_total))
            with month_col2: st.metric("Transactions", str(month_count))
            with month_col3: st.metric("Average", money(month_average))

            month_categories = monthly.get("categories", {})
            if month_categories:
                st.markdown('<div class="section-label">Where Your Money Goes</div>', unsafe_allow_html=True)
                st.caption("A simple breakdown of this month's spending.")

                month_category_series = pd.Series(month_categories, dtype="float64").sort_values(ascending=True)

                # HORIZONTAL PROGRESS BARS
                render_colored_bars(month_category_series)

                top_month_category = month_category_series.idxmax()
                top_month_amount = float(month_category_series.max())
                top_month_share = (top_month_amount / month_total * 100) if month_total > 0 else 0

                st.caption(str(top_month_category) + " is your biggest category at " + money(top_month_amount) + " (" + "{:.1f}%".format(top_month_share) + " of this month's spending).")

            if comparison is not None:
                previous_total = float(comparison.get("previous_month", {}).get("total_spending", 0))
                if previous_total > 0:
                    difference = month_total - previous_total
                    change = (difference / previous_total * 100)
                    if difference > 0:
                        st.info("You spent " + money(abs(difference)) + " more than last month " + "({:+.1f}%).".format(change))
                    elif difference < 0:
                        st.success("You spent " + money(abs(difference)) + " less than last month " + "({:+.1f}%).".format(change))
                    else:
                        st.info("Your spending is the same as last month.")

            month_highest = monthly.get("highest_expense")
            if month_highest:
                st.markdown('<div class="section-label">Biggest Expense</div>', unsafe_allow_html=True)
                highest_col1, highest_col2 = st.columns([2, 1], gap="medium")
                with highest_col1:
                    st.metric("Expense", str(month_highest.get("description", "-")))
                    st.caption("Your largest single expense this month.")
                with highest_col2:
                    st.metric("Amount", money(month_highest.get("amount", 0)))
                    st.caption("Category: " + str(month_highest.get("category", "-")))

        st.divider()

        # ====================================================
        # LAST 6 MONTHS
        # ====================================================

        st.markdown('<div class="section-label">Last 6 Months</div>', unsafe_allow_html=True)
        st.caption("See whether your overall spending is rising or falling.")

        trend = get_monthly_trend(6)

        if trend is None:
            st.warning("Six-month trend is currently unavailable.")
        else:
            trend_data = pd.DataFrame(trend.get("months", []))

            if trend_data.empty:
                st.info("Not enough data for a six-month trend.")
            else:
                trend_data["total_spending"] = pd.to_numeric(trend_data["total_spending"], errors="coerce").fillna(0)
                trend_data["label"] = trend_data["label"].astype(str)

                # LINE CHART (Styled with Altair)
                trend_df = trend_data[["label", "total_spending"]].copy()
                render_altair_line_chart(trend_df, "label", "total_spending", 300)

                highest_month = trend_data.loc[trend_data["total_spending"].idxmax()]
                lowest_month = trend_data.loc[trend_data["total_spending"].idxmin()]
                trend_total = float(trend_data["total_spending"].sum())
                trend_average = trend_total / len(trend_data)

                six_col1, six_col2, six_col3 = st.columns(3, gap="medium")
                with six_col1: st.metric("Average Monthly", money(trend_average))
                with six_col2:
                    st.metric("Highest Month", str(highest_month["label"]))
                    st.caption(money(highest_month["total_spending"]))
                with six_col3:
                    st.metric("Lowest Month", str(lowest_month["label"]))
                    st.caption(money(lowest_month["total_spending"]))

        st.divider()

        # ====================================================
        # THIS YEAR
        # ====================================================

        st.markdown('<div class="section-label">This Year</div>', unsafe_allow_html=True)
        st.caption("Your complete spending picture for " + str(now.year) + ".")

        year_data = expenses[expenses["created_at"] >= year_start].copy()
        year_total = float(year_data["amount"].sum())
        year_count = len(year_data)
        year_average = (year_total / year_count) if year_count > 0 else 0

        year_col1, year_col2, year_col3 = st.columns(3, gap="medium")
        with year_col1: st.metric("Yearly Spending", money(year_total))
        with year_col2: st.metric("Transactions", str(year_count))
        with year_col3: st.metric("Average Transaction", money(year_average))

        if year_data.empty:
            st.info("No expenses recorded this year.")
        else:
            yearly_monthly = (
                year_data.assign(Month=year_data["created_at"].dt.strftime("%b"))
                .groupby("Month")["amount"].sum()
            )
            month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            yearly_monthly = yearly_monthly.reindex(month_order, fill_value=0)

            st.markdown('<div class="section-label">Monthly Spending</div>', unsafe_allow_html=True)
            st.caption("See how much you spent each month this year.")

            # VERTICAL BAR CHART (Styled with Altair)
            yearly_monthly_df = yearly_monthly.reset_index()
            yearly_monthly_df.columns = ["Month", "amount"]
            render_altair_vertical_bar(yearly_monthly_df, "Month", "amount", 300)

            yearly_categories = year_data.groupby("category")["amount"].sum().sort_values(ascending=True)

            if not yearly_categories.empty:
                st.markdown('<div class="section-label">Yearly Spending by Category</div>', unsafe_allow_html=True)
                
                # HORIZONTAL PROGRESS BARS
                render_colored_bars(yearly_categories)

            highest_year_month = yearly_monthly.idxmax()
            highest_year_month_amount = float(yearly_monthly.max())
            st.caption("Highest spending month: " + highest_year_month + " · " + money(highest_year_month_amount))

        st.divider()

        # ====================================================
        # SPENDING PATTERNS
        # ====================================================

        st.markdown('<div class="section-label">Spending Patterns</div>', unsafe_allow_html=True)
        st.caption("Simple patterns found in your expense history.")

        if expenses.empty:
            st.info("Add more expenses to see your spending patterns.")
        else:
            valid_expenses = expenses.dropna(subset=["created_at", "amount"]).copy()

            if valid_expenses.empty:
                st.info("Not enough valid expense data yet.")
            else:
                category_frequency = valid_expenses["category"].value_counts()
                most_frequent_category = category_frequency.index[0]
                most_frequent_count = int(category_frequency.iloc[0])

                daily_totals = (
                    valid_expenses.assign(date_only=valid_expenses["created_at"].dt.date)
                    .groupby("date_only")["amount"].sum()
                )
                highest_day = daily_totals.idxmax()
                highest_day_amount = float(daily_totals.max())
                overall_average = float(valid_expenses["amount"].mean())
                spending_days = int(daily_totals.shape[0])

                pattern_col1, pattern_col2 = st.columns(2, gap="medium")
                with pattern_col1:
                    st.metric("Most Frequent Category", str(most_frequent_category))
                    st.caption(str(most_frequent_count) + " transaction" + ("s" if most_frequent_count != 1 else ""))
                with pattern_col2:
                    st.metric("Highest Spending Day", highest_day.strftime("%d %b %Y"))
                    st.caption(money(highest_day_amount) + " spent that day.")

                pattern_col3, pattern_col4 = st.columns(2, gap="medium")
                with pattern_col3: st.metric("Average Transaction", money(overall_average))
                with pattern_col4: st.metric("Spending Days", str(spending_days))

        st.divider()

        # ====================================================
        # WHAT STANDS OUT
        # ====================================================

        st.markdown('<div class="section-label">What Stands Out</div>', unsafe_allow_html=True)

        observations = []

        if today_count > 0:
            observations.append("You made " + str(today_count) + " transaction" + ("s" if today_count != 1 else "") + " today, totaling " + money(today_total) + ".")

        if monthly is not None and month_categories:
            observations.append(str(top_month_category) + " is your biggest category this month.")

        if comparison is not None:
            current_month_total = float(comparison.get("current_month", {}).get("total_spending", 0))
            previous_month_total = float(comparison.get("previous_month", {}).get("total_spending", 0))
            if previous_month_total > 0:
                if current_month_total > previous_month_total:
                    observations.append("You are spending more this month than last month.")
                elif current_month_total < previous_month_total:
                    observations.append("You are spending less this month than last month.")
                else:
                    observations.append("Your spending is similar to last month.")

        if year_count > 0:
            observations.append("You have spent " + money(year_total) + " so far this year.")

        if observations:
            for observation in observations[:3]:
                st.info(observation)
        else:
            st.info("Keep adding expenses to see useful spending patterns.")