import pandas as pd
import streamlit as st

def show_dashboard(get_summary, get_expenses, get_budget):

    st.markdown(
        '<div class="section-label">'
        'Overview'
        '</div>',
        unsafe_allow_html=True
    )

    summary = get_summary()

    expenses = get_expenses()

    if summary is None or expenses is None:

        st.error(
            "Unable to retrieve dashboard data."
        )

    elif len(expenses) == 0:

        st.info(
            "No expenses yet. Add your first expense."
        )

    else:

        total_spending = summary.get(
            "total_spending",
            0
        )

        total_expenses = summary.get(
            "total_expenses",
            0
        )

        if total_expenses > 0:

            average_expense = (
                total_spending
                / total_expenses
            )

        else:

            average_expense = 0

        metric1, metric2, metric3, metric4 = st.columns(
            4,
            gap="medium"
        )

        with metric1:

            st.metric(
                "Total Spending",
                "Rs. {:,.2f}".format(
                    total_spending
                )
            )

        with metric2:

            st.metric(
                "Expenses",
                str(
                    total_expenses
                )
            )

        with metric3:

            st.metric(
                "Average Expense",
                "Rs. {:,.2f}".format(
                    average_expense
                )
            )

        with metric4:

            st.metric(
                "Essential Spending",
                "Rs. {:,.2f}".format(
                    summary.get(
                        "essential_spending",
                        0
                    )
                )
            )

        budget = get_budget()

        if budget is not None and budget.get("monthly_budget", 0) > 0:

            st.markdown(
                '<div class="section-label">'
                'Budget Status'
                '</div>',
                unsafe_allow_html=True
            )

            budget_col1, budget_col2, budget_col3, budget_col4 = st.columns(
                4,
                gap="medium"
            )

            with budget_col1:
                st.metric(
                    "Monthly Budget",
                    "Rs. {:,.2f}".format(
                        budget["monthly_budget"]
                    )
                )

            with budget_col2:
                st.metric(
                    "Remaining",
                    "Rs. {:,.2f}".format(
                        budget["remaining"]
                    )
                )

            with budget_col3:
                st.metric(
                    "Budget Used",
                    "{:.1f}%".format(
                        budget["usage_percent"]
                    )
                )

            st.caption(
                "Regular spending is what counts toward the monthly budget. "
                "Essential / unexpected spending is tracked separately."
            )

            if budget["status"] == "Over budget":
                st.error(budget["alert"])
            elif budget["status"] in (
                "Near limit",
                "Watch spending"
            ):
                st.warning(budget["alert"])
            else:
                st.success(budget["alert"])

        essential_total = float(
            summary.get(
                "essential_spending",
                0
            )
        )

        essential_count = int(
            summary.get(
                "essential_expenses",
                0
            )
        )

        st.divider()

        

        st.markdown(
            '<div class="section-label">'
            'Spending by Category'
            '</div>',
            unsafe_allow_html=True
        )

        categories = summary.get(
            "categories",
            {}
        )

        if categories:

            category_summary = pd.Series(
                categories,
                dtype="float64"
            ).sort_values(
                ascending=False
            )

            # Calculate percentages
            total = category_summary.sum()
            category_percentages = (category_summary / total * 100).round(1)

            # Define colors for categories
            colors = {
                'Food': '#FF9F45',
                'Shopping': '#FF6B9D',
                'Transport': '#5A9FFF',
                'Entertainment': '#4FD3BE',
                'Education': '#A57FFF',
                'Health': '#FF6B6B',
                'Utilities': '#FFD93D',
                'Other': '#8B8B8B'
            }

            # Display each category with styled bar
            for idx, (category, amount) in enumerate(category_summary.items()):
                percentage = category_percentages[category]
                bar_color = colors.get(category, '#5A9FFF')

                st.markdown(
                    f'''
                    <div style="margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="color: #B8B8B8; font-size: 12px; font-weight: 500;">{category}</span>
                            <span style="color: #707070; font-size: 11px;">{percentage}%</span>
                        </div>
                        <div style="width: 100%; height: 8px; background: #303030; border-radius: 5px; overflow: hidden;">
                            <div style="width: {percentage}%; height: 100%; background: {bar_color}; border-radius: 5px; transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);"></div>
                        </div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No category information available."
            )

        st.divider()

        st.markdown(
                    '<div class="section-label">'
                    'Essential & Unexpected'
                    '</div>',
                    unsafe_allow_html=True
                )
        
        st.caption(
            "Important expenses are shown separately from regular spending."
        )
        
        if essential_total > 0:
                    st.metric(
                        "Essential Spending",
                        "Rs. {:,.2f}".format(
                            essential_total
                        ),
                        str(essential_count) + " expense"
                        + ("" if essential_count == 1 else "s")
                    )
        
                    essential_rows = expenses[
                        expenses.get(
                            "is_essential",
                            False
                        ).fillna(False).astype(bool)
                    ].copy() if "is_essential" in expenses.columns else pd.DataFrame()
        
                    if not essential_rows.empty:
                        essential_display = essential_rows[
                            [
                                "description",
                                "amount",
                                "category"
                            ]
                        ].rename(
                            columns={
                                "description": "Expense",
                                "amount": "Amount (Rs.)",
                                "category": "Category"
                            }
                        )
        
                        essential_display[
                            "Amount (Rs.)"
                        ] = essential_display[
                            "Amount (Rs.)"
                        ].round(2)
        
                    st.dataframe(
                        essential_display.head(5),
                        use_container_width=True,
                        hide_index=True
                    )
        else:
            st.info(
                "No essential or unexpected spending recorded."
            )
        
            st.divider()

        