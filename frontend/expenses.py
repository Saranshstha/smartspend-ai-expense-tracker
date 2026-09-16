import pandas as pd
import streamlit as st

def show_expenses(get_expenses, save_table_changes, delete_expense):


        st.markdown(
            '<div class="section-label">'
            'Expense History'
            '</div>',
            unsafe_allow_html=True
        )


        expenses = get_expenses()


        if expenses is None:

            st.error(
                "Unable to retrieve expenses."
            )


        elif len(expenses) == 0:

            st.info(
                "No expenses have been recorded yet."
            )


        else:

            # ====================================================
            # PREPARE DATA
            # ====================================================

            expenses = expenses.copy()


            expenses["amount"] = pd.to_numeric(
                expenses["amount"],
                errors="coerce"
            )


            expenses["confidence"] = pd.to_numeric(
                expenses["confidence"],
                errors="coerce"
            )


            expenses["created_at"] = pd.to_datetime(
                expenses["created_at"],
                errors="coerce",
                utc = True
            ).dt.tz_convert("Asia/Kathmandu")


            # ====================================================
            # FILTER & SORT
            # ====================================================

            st.markdown(
                '<div class="section-label">'
                'Filter & Sort'
                '</div>',
                unsafe_allow_html=True
            )


            filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(
                [1.7, 1, 1, 1],
                gap="medium"
            )


            # ----------------------------------------------------
            # SEARCH
            # ----------------------------------------------------

            with filter_col1:

                search = st.text_input(
                    "Search",
                    placeholder="Description or category...",
                    key="expense_search_input"
                )


            # ----------------------------------------------------
            # CATEGORY
            # ----------------------------------------------------

            with filter_col2:

                categories = [
                    "All"
                ] + sorted(
                    expenses[
                        "category"
                    ]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )


                selected_category = st.selectbox(
                    "Category",
                    categories,
                    key="expense_category_filter"
                )


            # ----------------------------------------------------
            # SORT
            # ----------------------------------------------------

            with filter_col3:

                sort_option = st.selectbox(
                    "Sort by",
                    [
                        "Newest",
                        "Oldest",
                        "Highest amount",
                        "Lowest amount",
                        "Highest confidence",
                        "Lowest confidence"
                    ],
                    key="expense_sort_option"
                )

            with filter_col4:

                type_options = [
                    "All",
                    "Regular Spending",
                    "Essential / Unexpected"
                ]

                selected_type = st.selectbox(
                    "Spending Type",
                    type_options,
                    key="expense_type_filter"
                )


            # ====================================================
            # SECOND FILTER ROW
            # ====================================================

            filter_col4, filter_col5, filter_col6 = st.columns(
                [1, 1, 1],
                gap="medium"
            )


            # ----------------------------------------------------
            # DATE
            # ----------------------------------------------------

            with filter_col4:

                date_options = [
                    "All time",
                    "Today",
                    "Last 7 days",
                    "Last 30 days",
                    "This month"
                ]


                selected_date = st.selectbox(
                    "Date",
                    date_options,
                    key="expense_date_filter"
                )


            # ----------------------------------------------------
            # MINIMUM AMOUNT
            # ----------------------------------------------------

            with filter_col5:

                minimum_amount = st.number_input(
                    "Minimum amount",
                    min_value=0.0,
                    value=0.0,
                    step=50.0,
                    format="%.2f",
                    key="expense_min_amount"
                )


            # ----------------------------------------------------
            # MAXIMUM AMOUNT
            # ----------------------------------------------------

            with filter_col6:

                maximum_amount = st.number_input(
                    "Maximum amount",
                    min_value=0.0,
                    value=0.0,
                    step=50.0,
                    format="%.2f",
                    key="expense_max_amount"
                )


            # ====================================================
            # APPLY SEARCH
            # ====================================================

            filtered = expenses.copy()


            if search.strip():

                search_lower = (
                    search
                    .strip()
                    .lower()
                )


                description_match = (
                    filtered[
                        "description"
                    ]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        search_lower,
                        na=False,
                        regex=False
                    )
                )


                category_match = (
                    filtered[
                        "category"
                    ]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        search_lower,
                        na=False,
                        regex=False
                    )
                )


                filtered = filtered[
                    description_match
                    | category_match
                ]


            # ====================================================
            # APPLY CATEGORY
            # ====================================================

            if selected_category != "All":

                filtered = filtered[
                    filtered[
                        "category"
                    ]
                    == selected_category
                ]


            # ====================================================
            # APPLY SPENDING TYPE
            # ====================================================

            if selected_type != "All":

                type_value = (
                    selected_type
                    == "Essential / Unexpected"
                )

                filtered = filtered[
                    filtered["is_essential"].fillna(False).astype(bool)
                    == type_value
                ]


            # ====================================================
            # APPLY DATE
            # ====================================================

            current_time = pd.Timestamp.now(
                tz="Asia/Kathmandu"
            )


            if selected_date == "Today":

                today = current_time.normalize()

                filtered = filtered[
                    filtered[
                        "created_at"
                    ] >= today
                ]


            elif selected_date == "Last 7 days":

                seven_days_ago = (
                    current_time
                    - pd.Timedelta(days=7)
                )

                filtered = filtered[
                    filtered[
                        "created_at"
                    ] >= seven_days_ago
                ]


            elif selected_date == "Last 30 days":

                thirty_days_ago = (
                    current_time
                    - pd.Timedelta(days=30)
                )

                filtered = filtered[
                    filtered[
                        "created_at"
                    ] >= thirty_days_ago
                ]


            elif selected_date == "This month":

                month_start = pd.Timestamp(
                    current_time.year,
                    current_time.month,
                    1,
                    tz="Asia/Kathmandu"
                )

                filtered = filtered[
                    filtered[
                        "created_at"
                    ] >= month_start
                ]


            # ====================================================
            # APPLY AMOUNT RANGE
            # ====================================================

            if minimum_amount > 0:

                filtered = filtered[
                    filtered[
                        "amount"
                    ] >= minimum_amount
                ]


            if maximum_amount > 0:

                if maximum_amount < minimum_amount:

                    st.warning(
                        "Maximum amount cannot be lower "
                        "than minimum amount."
                    )

                else:

                    filtered = filtered[
                        filtered[
                            "amount"
                        ] <= maximum_amount
                    ]


            # ====================================================
            # SORT
            # ====================================================

            if sort_option == "Newest":

                filtered = filtered.sort_values(
                    "created_at",
                    ascending=False
                )


            elif sort_option == "Oldest":

                filtered = filtered.sort_values(
                    "created_at",
                    ascending=True
                )


            elif sort_option == "Highest amount":

                filtered = filtered.sort_values(
                    "amount",
                    ascending=False
                )


            elif sort_option == "Lowest amount":

                filtered = filtered.sort_values(
                    "amount",
                    ascending=True
                )


            elif sort_option == "Highest confidence":

                filtered = filtered.sort_values(
                    "confidence",
                    ascending=False
                )


            elif sort_option == "Lowest confidence":

                filtered = filtered.sort_values(
                    "confidence",
                    ascending=True
                )


            # ====================================================
            # RESULT SUMMARY
            # ====================================================

            total_records = len(
                expenses
            )


            filtered_records = len(
                filtered
            )


            filtered_total = filtered[
                "amount"
            ].sum()


            if filtered_records > 0:

                filtered_average = (
                    filtered_total
                    / filtered_records
                )

            else:

                filtered_average = 0


            summary_col1, summary_col2, summary_col3 = (
                st.columns(
                    3,
                    gap="medium"
                )
            )


            with summary_col1:

                st.metric(
                    "Showing",
                    str(
                        filtered_records
                    )
                    + " / "
                    + str(
                        total_records
                    )
                )


            with summary_col2:

                st.metric(
                    "Filtered Spending",
                    "Rs. {:,.2f}".format(
                        filtered_total
                    )
                )


            with summary_col3:

                st.metric(
                    "Average",
                    "Rs. {:,.2f}".format(
                        filtered_average
                    )
                )


            # ====================================================
            # EXPENSE TABLE
            # ====================================================

            if len(filtered) == 0:

                st.info(
                    "No expenses match your current "
                    "search and filter settings."
                )


            else:

                st.divider()


                st.markdown(
                    '<div class="section-label">'
                    'Expense Records'
                    '</div>',
                    unsafe_allow_html=True
                )


                st.caption(
                    "Edit Description or Amount directly "
                    "in the table. Category and Confidence "
                    "are generated by the AI model. "
                    "Changing a description will recalculate "
                    "its category when you save the changes."
                )


                editable_table = filtered[
                    [
                        "id",
                        "description",
                        "amount",
                        "category",
                        "confidence",
                        "is_essential",
                        "created_at"
                    ]
                ].copy()


                editable_table = (
                    editable_table
                    .rename(
                        columns={
                            "id": "ID",
                            "description": "Description",
                            "amount": "Amount (Rs.)",
                            "category": "Category",
                            "confidence": "Confidence (%)",
                            "is_essential": "Type",
                            "created_at": "Date"
                        }
                    )
                )


                editable_table[
                    "Amount (Rs.)"
                ] = (
                    editable_table[
                        "Amount (Rs.)"
                    ]
                    .round(2)
                )


                editable_table[
                    "Confidence (%)"
                ] = (
                    editable_table[
                        "Confidence (%)"
                    ]
                    .round(2)
                )


                editable_table[
                    "Type"
                ] = editable_table[
                    "Type"
                ].apply(
                    lambda value:
                    "Essential / Unexpected"
                    if bool(value)
                    else "Regular Spending"
                )

                editable_table[
                    "Date"
                ] = (
                    editable_table[
                        "Date"
                    ]
                    .dt.strftime(
                        "%Y-%m-%d %H:%M"
                    )
                )


                # =================================================
                # EDITABLE TABLE
                # =================================================

                edited_table = st.data_editor(
                    editable_table,

                    use_container_width=True,

                    hide_index=True,

                    num_rows="fixed",

                    disabled=[
                        "ID",
                        "Category",
                        "Confidence (%)",
                        "Date"
                    ],

                    column_config={

                        "ID": st.column_config.NumberColumn(
                            "ID",
                            disabled=True
                        ),

                        "Description": st.column_config.TextColumn(
                            "Description",
                            required=True
                        ),

                        "Amount (Rs.)": st.column_config.NumberColumn(
                            "Amount (Rs.)",
                            min_value=0.01,
                            step=50.0,
                            format="%.2f",
                            required=True
                        ),

                        "Category": st.column_config.TextColumn(
                            "Category",
                            disabled=True
                        ),

                        "Confidence (%)": st.column_config.NumberColumn(
                            "Confidence (%)",
                            format="%.2f",
                            disabled=True
                        ),

                        "Type": st.column_config.SelectboxColumn(
                            "Type",
                            options=[
                                "Regular Spending",
                                "Essential / Unexpected"
                            ],
                            required=True
                        ),

                        "Date": st.column_config.TextColumn(
                            "Date",
                            disabled=True
                        )
                    },

                    key="expense_editor"
                )


                st.markdown("")


                # =================================================
                # SAVE CHANGES
                # =================================================

                if st.button(
                    "Save Changes",
                    type="primary",
                    use_container_width=True,
                    key="save_table_changes_button"
                ):

                    update_payload = []

                    validation_error = None


                    for _, row in edited_table.iterrows():

                        description_value = str(
                            row[
                                "Description"
                            ]
                        ).strip()


                        try:

                            amount_value = float(
                                row[
                                    "Amount (Rs.)"
                                ]
                            )

                        except Exception:

                            validation_error = (
                                "Amount must be a valid number."
                            )

                            break


                        if description_value == "":

                            validation_error = (
                                "Description cannot be empty."
                            )

                            break


                        if len(description_value) < 2:

                            validation_error = (
                                "Description must contain "
                                "at least 2 characters."
                            )

                            break


                        if amount_value <= 0:

                            validation_error = (
                                "Amount must be greater than 0."
                            )

                            break


                        update_payload.append(
                            {
                                "id": int(
                                    row[
                                        "ID"
                                    ]
                                ),

                                "description": (
                                    description_value
                                ),

                                "amount": (
                                    amount_value
                                ),

                                "is_essential": (
                                    str(
                                        row["Type"]
                                    ).strip()
                                    == "Essential / Unexpected"
                                )
                            }
                        )


                    if validation_error:

                        st.error(
                            validation_error
                        )


                    else:

                        success, result = (
                            save_table_changes(
                                update_payload
                            )
                        )


                        if success:

                            st.success(
                                "Expenses updated successfully."
                            )

                            st.info(
                                "Changed descriptions were "
                                "automatically re-categorized "
                                "by the AI model."
                            )

                            st.rerun()


                        else:

                            st.error(
                                result
                            )


            # ====================================================
            # DELETE EXPENSE
            # ====================================================

            st.divider()


            st.markdown(
                '<div class="section-label">'
                'Delete Expense'
                '</div>',
                unsafe_allow_html=True
            )


            delete_lookup = (
                expenses
                .set_index("id")
                .to_dict("index")
            )


            selected_delete_id = st.selectbox(
                "Select expense to delete",

                expenses[
                    "id"
                ].tolist(),

                format_func=lambda expense_id: (
                    str(
                        delete_lookup[
                            expense_id
                        ][
                            "description"
                        ]
                    )
                    + " — Rs. "
                    + format(
                        float(
                            delete_lookup[
                                expense_id
                            ][
                                "amount"
                            ]
                        ),
                        ".2f"
                    )
                ),

                key="delete_expense_selector"
            )


            if st.button(
                "Delete Selected Expense",
                key="delete_expense_button"
            ):

                st.session_state.confirm_delete = True


            # ====================================================
            # DELETE CONFIRMATION
            # ====================================================

            if st.session_state.confirm_delete:

                st.warning(
                    "Are you sure you want to delete this expense?"
                )


                confirm_col, cancel_col = st.columns(
                    2,
                    gap="medium"
                )


                with confirm_col:

                    if st.button(
                        "Yes, Delete",
                        type="primary",
                        use_container_width=True,
                        key="confirm_delete_button"
                    ):

                        deleted, message = (
                            delete_expense(
                                selected_delete_id
                            )
                        )


                        if deleted:

                            st.session_state.confirm_delete = False

                            st.session_state.prediction_result = None

                            st.success(
                                "Expense moved to Recently Deleted."
                            )

                            st.rerun()


                        else:

                            st.error(
                                message
                            )


                with cancel_col:

                    if st.button(
                        "Cancel",
                        use_container_width=True,
                        key="cancel_delete_button"
                    ):

                        st.session_state.confirm_delete = False

                        st.rerun()


     
