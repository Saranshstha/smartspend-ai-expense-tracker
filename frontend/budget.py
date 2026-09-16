import streamlit as st

def show_budget(get_budget, save_budget):


        st.markdown(
            '<div class="section-label">'
            'Budget & Spending Alerts'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Set a monthly limit and get a simple warning before spending gets out of control."
        )

        budget = get_budget()

        if budget is None:

            st.error(
                "Unable to retrieve budget information."
            )

        else:

            current_budget = float(
                budget.get(
                    "monthly_budget",
                    0
                )
            )

            budget_input = st.number_input(
                "Monthly budget (Rs.)",
                min_value=1.0,
                value=max(
                    1.0,
                    current_budget
                ),
                step=1000.0,
                format="%.2f",
                key="monthly_budget_input"
            )

            if st.button(
                "Save Monthly Budget",
                type="primary",
                use_container_width=True,
                key="save_monthly_budget_button"
            ):

                success, result = save_budget(
                    budget_input
                )

                if success:
                    st.success(
                        "Monthly budget saved successfully."
                    )
                    st.rerun()
                else:
                    st.error(result)

            st.divider()

            if current_budget <= 0:

                st.info(
                    "Set a monthly budget to start tracking your spending."
                )

            else:

                budget_col1, budget_col2, budget_col3, budget_col4 = st.columns(
                    4,
                    gap="medium"
                )

                with budget_col1:
                    st.metric(
                        "Spent This Month",
                        "Rs. {:,.2f}".format(
                            budget["spent"]
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

                with budget_col4:
                    st.metric(
                        "Essential Spending",
                        "Rs. {:,.2f}".format(
                            budget.get("essential_spending", 0)
                        )
                    )

                st.progress(
                    min(
                        budget["usage_percent"] / 100,
                        1.0
                    )
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

                st.divider()

                st.markdown(
                    '<div class="section-label">'
                    'Spending Forecast'
                    '</div>',
                    unsafe_allow_html=True
                )

                forecast_col1, forecast_col2 = st.columns(
                    2,
                    gap="medium"
                )

                with forecast_col1:
                    st.metric(
                        "Projected Month-End",
                        "Rs. {:,.2f}".format(
                            budget["projected_spending"]
                        )
                    )

                with forecast_col2:
                    if budget["projected_over_budget"] > 0:
                        st.metric(
                            "Projected Over Budget",
                            "Rs. {:,.2f}".format(
                                budget["projected_over_budget"]
                            )
                        )
                    else:
                        st.metric(
                            "Projected Over Budget",
                            "Rs. 0.00"
                        )

                st.caption(
                    "Forecast uses your average daily spending so far this month."
                )


     
