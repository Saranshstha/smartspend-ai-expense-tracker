import streamlit as st

def show_add_expense(add_expense):


        st.markdown(
            '<div class="section-label">'
            'Add Expense'
            '</div>',
            unsafe_allow_html=True
        )


        input_col, prediction_col = st.columns(
            [1.25, 0.85],
            gap="medium"
        )


        with input_col:

            description = st.text_input(
                "Description",
                placeholder="e.g. Lunch at a restaurant",
                key="description_input"
            )


            amount = st.number_input(
                "Amount (Rs.)",
                min_value=0.0,
                step=50.0,
                format="%.2f",
                key="amount_input"
            )

            spending_type = st.radio(
                "Spending Type",
                [
                    "Regular Spending",
                    "Essential / Unexpected"
                ],
                index=0,
                horizontal=True,
                key="spending_type_input"
            )

            is_essential = (
                spending_type == "Essential / Unexpected"
            )

            predict_clicked = st.button(
                "Predict Expense",
                type="primary",
                use_container_width=True,
                key="predict_expense_button"
            )


        with prediction_col:

            st.subheader(
                "AI Prediction"
            )


            if st.session_state.prediction_result is None:

                st.write(
                    "Ready"
                )


                st.caption(
                    "Enter an expense to get a prediction."
                )


            else:

                prediction = (
                    st.session_state.prediction_result
                )


                st.metric(
                    "Category",
                    prediction["category"]
                )


                st.caption(
                    "Confidence: "
                    + str(
                        prediction["confidence"]
                    )
                    + "%"
                )

                st.caption(
                    "Type: "
                    + (
                        "Essential / Unexpected"
                        if prediction.get("is_essential")
                        else "Regular Spending"
                    )
                )


                if prediction.get(
                    "created_at"
                ):

                    st.caption(
                        "Saved: "
                        + prediction[
                            "created_at"
                        ].replace(
                            "T",
                            " "
                        )
                    )


        if predict_clicked:

            if description.strip() == "":

                st.warning(
                    "Please enter an expense description."
                )


            elif amount <= 0:

                st.warning(
                    "Please enter an amount greater than 0."
                )


            else:

                result = add_expense(
                    description.strip(),
                    amount,
                    is_essential
                )


                if "error" in result:

                    st.error(
                        result["error"]
                    )


                else:

                    st.session_state.prediction_result = result

                    st.session_state.clear_inputs = True

                    st.success(
                        "Expense added successfully."
                    )

                    st.rerun()


     
