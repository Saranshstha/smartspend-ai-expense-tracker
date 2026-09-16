import pandas as pd
import streamlit as st

def show_recently_deleted(get_deleted_expenses, restore_expense):


        st.markdown(
            '<div class="section-label">'
            'Recently Deleted'
            '</div>',
            unsafe_allow_html=True
        )


        st.caption(
            "Deleted expenses can be restored for up to 15 days."
        )


        deleted_expenses = get_deleted_expenses()


        if deleted_expenses is None:

            st.error(
                "Unable to retrieve deleted expenses."
            )


        elif deleted_expenses.empty:

            st.info(
                "No deleted expenses are available."
            )


        else:

            deleted_expenses[
                "deleted_at"
            ] = pd.to_datetime(
                deleted_expenses[
                    "deleted_at"
                ],
                utc=True,
                errors="coerce"
            )


            now = pd.Timestamp.now(
                tz="UTC"
            )


            deleted_expenses[
                "Days remaining"
            ] = deleted_expenses[
                "deleted_at"
            ].apply(
                lambda deleted_at: max(
                    0,
                    int(
                        (
                            deleted_at
                            + pd.Timedelta(days=15)
                            - now
                        ).total_seconds()
                        // 86400
                    )
                    + 1
                )
                if pd.notna(deleted_at)
                else 0
            )


            deleted_expenses[
                "Deleted on"
            ] = (
                deleted_expenses[
                    "deleted_at"
                ]
                .dt.tz_convert(
                    "Asia/Kathmandu"
                )
                .dt.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )


            total_deleted = len(
                deleted_expenses
            )


            total_deleted_amount = (
                deleted_expenses[
                    "amount"
                ]
                .sum()
            )


            metric1, metric2 = st.columns(
                2,
                gap="medium"
            )


            with metric1:

                st.metric(
                    "Deleted Expenses",
                    str(
                        total_deleted
                    )
                )


            with metric2:

                st.metric(
                    "Deleted Amount",
                    "Rs. {:,.2f}".format(
                        total_deleted_amount
                    )
                )


            st.divider()


            display_deleted = deleted_expenses[
                [
                    "description",
                    "amount",
                    "category",
                    "Deleted on",
                    "Days remaining"
                ]
            ].copy()


            display_deleted = display_deleted.rename(
                columns={
                    "description": "Description",
                    "amount": "Amount (Rs.)",
                    "category": "Category"
                }
            )


            display_deleted[
                "Amount (Rs.)"
            ] = (
                display_deleted[
                    "Amount (Rs.)"
                ]
                .round(2)
            )


            st.dataframe(
                display_deleted,
                use_container_width=True,
                hide_index=True
            )


            st.divider()


            deleted_lookup = (
                deleted_expenses
                .set_index("id")
                .to_dict("index")
            )


            restore_id = st.selectbox(
                "Select expense to restore",

                deleted_expenses[
                    "id"
                ].tolist(),

                format_func=lambda expense_id: (
                    str(
                        deleted_lookup[
                            expense_id
                        ][
                            "description"
                        ]
                    )
                    + " - Rs. "
                    + format(
                        float(
                            deleted_lookup[
                                expense_id
                            ][
                                "amount"
                            ]
                        ),
                        ".2f"
                    )
                ),

                key="restore_expense_selector"
            )


            if st.button(
                "Restore Selected Expense",
                type="primary",
                use_container_width=True,
                key="restore_expense_button"
            ):

                restored, message = (
                    restore_expense(
                        restore_id
                    )
                )


                if restored:

                    st.success(
                        "Expense restored successfully."
                    )

                    st.rerun()


                else:

                    st.error(
                        message
                    )


     
