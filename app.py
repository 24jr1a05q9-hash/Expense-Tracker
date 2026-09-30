import json
import os
import uuid
from datetime import date, datetime

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# FILE SETTINGS
# ============================================================

DATA_FILE = "expenses.json"

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Education",
    "Entertainment",
    "Health",
    "Travel",
    "Other"
]

PAYMENT_METHODS = [
    "Cash",
    "UPI",
    "Credit Card",
    "Debit Card",
    "Bank Transfer"
]


# ============================================================
# SIMPLE PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
    <style>
    
    .main {
        background-color: #f7f9fc;
    }

    h1, h2, h3 {
        font-weight: 800 !important;
    }

    p, label {
        font-weight: 600 !important;
    }

    .main-title {
        font-size: 40px;
        font-weight: 900;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 25px;
    }

    .card {
        padding: 20px;
        border-radius: 16px;
        background-color: white;
        border: 1px solid #e5e7eb;
        box-shadow: 0 5px 20px rgba(0,0,0,0.06);
    }

    .card:hover {
        transform: translateY(-3px);
        transition: 0.2s;
        box-shadow: 0 10px 25px rgba(0,0,0,0.10);
    }

    .card-title {
        font-size: 14px;
        font-weight: 800;
        color: #64748b;
    }

    .card-value {
        font-size: 28px;
        font-weight: 900;
        margin-top: 8px;
        color: #111827;
    }

    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        border-radius: 15px;
        background-color: #111827;
        color: white;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD JSON
# ============================================================

def load_expenses():

    if not os.path.exists(DATA_FILE):

        try:
            with open(
                DATA_FILE,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump([], file, indent=4)

        except OSError:
            return []

        return []

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except json.JSONDecodeError:

        st.error(
            "expenses.json contains invalid JSON."
        )

        return []

    except OSError as error:

        st.error(
            f"Unable to read expenses.json: {error}"
        )

        return []


# ============================================================
# SAVE JSON
# ============================================================

def save_expenses(expenses):

    try:

        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                expenses,
                file,
                indent=4
            )

        return True

    except OSError as error:

        st.error(
            f"Unable to save data: {error}"
        )

        return False


# ============================================================
# SESSION STATE
# ============================================================

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

if "delete_id" not in st.session_state:
    st.session_state.delete_id = None


# ============================================================
# DATAFRAME
# ============================================================

def get_dataframe():

    if not st.session_state.expenses:

        return pd.DataFrame(
            columns=[
                "id",
                "category",
                "amount",
                "date",
                "description",
                "payment_method"
            ]
        )

    df = pd.DataFrame(
        st.session_state.expenses
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    ).fillna(0)

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    return df


# ============================================================
# ADD EXPENSE
# ============================================================

def add_expense(
    category,
    amount,
    expense_date,
    description,
    payment_method
):

    expense = {
        "id": str(uuid.uuid4()),
        "category": category,
        "amount": float(amount),
        "date": expense_date.isoformat(),
        "description": description.strip(),
        "payment_method": payment_method
    }

    st.session_state.expenses.append(
        expense
    )

    return save_expenses(
        st.session_state.expenses
    )


# ============================================================
# UPDATE EXPENSE
# ============================================================

def update_expense(
    expense_id,
    category,
    amount,
    expense_date,
    description,
    payment_method
):

    for expense in st.session_state.expenses:

        if expense["id"] == expense_id:

            expense["category"] = category
            expense["amount"] = float(amount)
            expense["date"] = expense_date.isoformat()
            expense["description"] = description.strip()
            expense["payment_method"] = payment_method

            return save_expenses(
                st.session_state.expenses
            )

    return False


# ============================================================
# DELETE EXPENSE
# ============================================================

def delete_expense(expense_id):

    old_count = len(
        st.session_state.expenses
    )

    st.session_state.expenses = [
        expense
        for expense in st.session_state.expenses
        if expense["id"] != expense_id
    ]

    if len(
        st.session_state.expenses
    ) < old_count:

        return save_expenses(
            st.session_state.expenses
        )

    return False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("💰 Expense Tracker")

    st.write(
        "**Professional Finance Dashboard**"
    )

    st.divider()

    page = st.radio(
        "MENU",
        [
            "📊 Dashboard",
            "➕ Add Expense",
            "📋 Manage Expenses"
        ],
        key="page_navigation"
    )

    st.divider()

    st.write("### 👨‍💻 Developer")

    st.write(
        "**Sheik Mohammad Riyaaz**"
    )

    st.write(
        "B.Tech CSE • 3rd Year"
    )


# ============================================================
# DATA
# ============================================================

df = get_dataframe()


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.markdown(
        '<div class="main-title">'
        '💰 Expense Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Track your spending, understand your habits, '
        'and manage your expenses easily.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    total = (
        float(df["amount"].sum())
        if not df.empty
        else 0
    )

    count = len(df)

    average = (
        float(df["amount"].mean())
        if not df.empty
        else 0
    )

    highest = (
        float(df["amount"].max())
        if not df.empty
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "💰 Total Spending",
            f"₹{total:,.2f}"
        )

    with c2:

        st.metric(
            "🧾 Transactions",
            count
        )

    with c3:

        st.metric(
            "📈 Average Expense",
            f"₹{average:,.2f}"
        )

    with c4:

        st.metric(
            "🔥 Highest Expense",
            f"₹{highest:,.2f}"
        )

    st.divider()

    # --------------------------------------------------------
    # EMPTY DATA
    # --------------------------------------------------------

    if df.empty:

        st.info(
            "Your dashboard is ready! "
            "Add your first expense to start seeing analytics."
        )

        st.markdown(
            "### 🚀 Get Started"
        )

        st.write(
            "Use **Add Expense** from the sidebar "
            "to create your first transaction."
        )

    else:

        # ----------------------------------------------------
        # CHARTS
        # ----------------------------------------------------

        st.subheader(
            "📊 Expense Analytics"
        )

        chart1, chart2 = st.columns(2)

        with chart1:

            category_data = (
                df.groupby(
                    "category",
                    as_index=False
                )["amount"]
                .sum()
                .sort_values(
                    "amount",
                    ascending=False
                )
            )

            fig1 = px.bar(
                category_data,
                x="category",
                y="amount",
                title="Spending by Category",
                text_auto=".2f"
            )

            fig1.update_layout(
                height=400,
                template="plotly_white"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

        with chart2:

            payment_data = (
                df.groupby(
                    "payment_method",
                    as_index=False
                )["amount"]
                .sum()
            )

            fig2 = px.pie(
                payment_data,
                names="payment_method",
                values="amount",
                title="Payment Method Distribution",
                hole=0.45
            )

            fig2.update_layout(
                height=400,
                template="plotly_white"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        # ----------------------------------------------------
        # MONTHLY CHART
        # ----------------------------------------------------

        valid_dates = df.dropna(
            subset=["date"]
        ).copy()

        if not valid_dates.empty:

            valid_dates["month"] = (
                valid_dates["date"]
                .dt.to_period("M")
                .astype(str)
            )

            monthly = (
                valid_dates
                .groupby(
                    "month",
                    as_index=False
                )["amount"]
                .sum()
            )

            fig3 = px.line(
                monthly,
                x="month",
                y="amount",
                markers=True,
                title="Monthly Spending Trend"
            )

            fig3.update_layout(
                height=400,
                template="plotly_white"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

        # ----------------------------------------------------
        # RECENT TRANSACTIONS
        # ----------------------------------------------------

        st.subheader(
            "🕒 Recent Transactions"
        )

        recent = (
            df.sort_values(
                "date",
                ascending=False
            )
            .head(5)
            .copy()
        )

        recent["date"] = (
            recent["date"]
            .dt.strftime("%d-%m-%Y")
        )

        recent["amount"] = (
            recent["amount"]
            .map(
                lambda x:
                f"₹{x:,.2f}"
            )
        )

        recent = recent[
            [
                "date",
                "category",
                "description",
                "payment_method",
                "amount"
            ]
        ]

        recent.columns = [
            "Date",
            "Category",
            "Description",
            "Payment Method",
            "Amount"
        ]

        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ADD EXPENSE
# ============================================================

elif page == "➕ Add Expense":

    st.title(
        "➕ Add New Expense"
    )

    st.write(
        "Enter your transaction details below."
    )

    st.divider()

    with st.form(
        "add_expense_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            category = st.selectbox(
                "Category",
                CATEGORIES,
                key="new_category"
            )

            amount = st.number_input(
                "Amount (₹)",
                min_value=0.01,
                step=0.01,
                format="%.2f",
                key="new_amount"
            )

            expense_date = st.date_input(
                "Date",
                value=date.today(),
                key="new_date"
            )

        with col2:

            payment = st.selectbox(
                "Payment Method",
                PAYMENT_METHODS,
                key="new_payment"
            )

            description = st.text_area(
                "Description",
                placeholder="Example: Lunch at college",
                key="new_description"
            )

        submit = st.form_submit_button(
            "💾 Save Expense",
            use_container_width=True
        )

        if submit:

            if amount <= 0:

                st.error(
                    "Amount must be greater than ₹0."
                )

            elif not description.strip():

                st.error(
                    "Please enter a description."
                )

            else:

                success = add_expense(
                    category,
                    amount,
                    expense_date,
                    description,
                    payment
                )

                if success:

                    st.success(
                        "✅ Expense added successfully!"
                    )

                    st.balloons()


# ============================================================
# MANAGE EXPENSES
# ============================================================

elif page == "📋 Manage Expenses":

    st.title(
        "📋 Manage Expenses"
    )

    st.write(
        "Search, filter, edit and delete your transactions."
    )

    st.divider()

    if df.empty:

        st.info(
            "No expenses available. "
            "Please add an expense first."
        )

    else:

        # ----------------------------------------------------
        # FILTERS
        # ----------------------------------------------------

        st.subheader(
            "🔎 Search & Filters"
        )

        f1, f2, f3 = st.columns(3)

        with f1:

            search = st.text_input(
                "Search",
                placeholder="Search category or description...",
                key="search_expenses"
            )

        with f2:

            category_filter = st.selectbox(
                "Category",
                ["All"] + CATEGORIES,
                key="filter_category"
            )

        with f3:

            payment_filter = st.selectbox(
                "Payment Method",
                ["All"] + PAYMENT_METHODS,
                key="filter_payment"
            )

        filtered = df.copy()

        if search.strip():

            text = search.strip().lower()

            filtered = filtered[
                filtered["description"]
                .str.lower()
                .str.contains(
                    text,
                    na=False
                )
                |
                filtered["category"]
                .str.lower()
                .str.contains(
                    text,
                    na=False
                )
            ]

        if category_filter != "All":

            filtered = filtered[
                filtered["category"]
                == category_filter
            ]

        if payment_filter != "All":

            filtered = filtered[
                filtered["payment_method"]
                == payment_filter
            ]

        st.write(
            f"**{len(filtered)} transaction(s) found**"
        )

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        if not filtered.empty:

            table = filtered.copy()

            table["date"] = (
                table["date"]
                .dt.strftime("%d-%m-%Y")
            )

            table["amount"] = (
                table["amount"]
                .map(
                    lambda x:
                    f"₹{x:,.2f}"
                )
            )

            table = table[
                [
                    "date",
                    "category",
                    "description",
                    "payment_method",
                    "amount"
                ]
            ]

            table.columns = [
                "Date",
                "Category",
                "Description",
                "Payment Method",
                "Amount"
            ]

            st.dataframe(
                table,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No expenses match your filters."
            )

        st.divider()

        # ----------------------------------------------------
        # ACTIONS
        # ----------------------------------------------------

        st.subheader(
            "⚙️ Manage Transaction"
        )

        options = {}

        for expense in st.session_state.expenses:

            label = (
                f"{expense.get('date', '')} | "
                f"{expense.get('category', '')} | "
                f"₹{float(expense.get('amount', 0)):,.2f} | "
                f"{expense.get('description', '')}"
            )

            options[label] = expense["id"]

        selected_label = st.selectbox(
            "Select an expense",
            list(options.keys()),
            key="selected_expense"
        )

        selected_id = options[
            selected_label
        ]

        edit_col, delete_col = st.columns(2)

        with edit_col:

            if st.button(
                "✏️ Edit Expense",
                use_container_width=True,
                key="edit_expense"
            ):

                st.session_state.editing_id = (
                    selected_id
                )

                st.rerun()

        with delete_col:

            if st.button(
                "🗑️ Delete Expense",
                use_container_width=True,
                key="delete_expense"
            ):

                st.session_state.delete_id = (
                    selected_id
                )

                st.rerun()

        # ----------------------------------------------------
        # DELETE CONFIRMATION
        # ----------------------------------------------------

        if st.session_state.delete_id:

            st.warning(
                "⚠️ Are you sure you want to delete this expense?"
            )

            yes_col, no_col = st.columns(2)

            with yes_col:

                if st.button(
                    "✅ Yes, Delete",
                    use_container_width=True,
                    key="confirm_delete"
                ):

                    success = delete_expense(
                        st.session_state.delete_id
                    )

                    st.session_state.delete_id = None

                    if success:

                        st.success(
                            "Expense deleted successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Could not delete the expense."
                        )

            with no_col:

                if st.button(
                    "❌ Cancel",
                    use_container_width=True,
                    key="cancel_delete"
                ):

                    st.session_state.delete_id = None

                    st.rerun()

        # ----------------------------------------------------
        # EDIT FORM
        # ----------------------------------------------------

        if st.session_state.editing_id:

            expense = next(
                (
                    item
                    for item in st.session_state.expenses
                    if item["id"]
                    == st.session_state.editing_id
                ),
                None
            )

            if expense:

                st.divider()

                st.subheader(
                    "✏️ Edit Expense"
                )

                try:

                    existing_date = datetime.strptime(
                        expense["date"],
                        "%Y-%m-%d"
                    ).date()

                except (
                    ValueError,
                    TypeError
                ):

                    existing_date = date.today()

                category_index = (
                    CATEGORIES.index(
                        expense["category"]
                    )
                    if expense["category"]
                    in CATEGORIES
                    else 0
                )

                payment_index = (
                    PAYMENT_METHODS.index(
                        expense["payment_method"]
                    )
                    if expense["payment_method"]
                    in PAYMENT_METHODS
                    else 0
                )

                with st.form(
                    "edit_expense_form"
                ):

                    e1, e2 = st.columns(2)

                    with e1:

                        edit_category = st.selectbox(
                            "Category",
                            CATEGORIES,
                            index=category_index,
                            key="edit_category"
                        )

                        edit_amount = st.number_input(
                            "Amount (₹)",
                            min_value=0.01,
                            value=max(
                                float(
                                    expense["amount"]
                                ),
                                0.01
                            ),
                            step=0.01,
                            format="%.2f",
                            key="edit_amount"
                        )

                        edit_date = st.date_input(
                            "Date",
                            value=existing_date,
                            key="edit_date"
                        )

                    with e2:

                        edit_payment = st.selectbox(
                            "Payment Method",
                            PAYMENT_METHODS,
                            index=payment_index,
                            key="edit_payment"
                        )

                        edit_description = st.text_area(
                            "Description",
                            value=expense.get(
                                "description",
                                ""
                            ),
                            key="edit_description"
                        )

                    save_col, cancel_col = st.columns(2)

                    with save_col:

                        save_button = st.form_submit_button(
                            "💾 Save Changes",
                            use_container_width=True
                        )

                    with cancel_col:

                        cancel_button = st.form_submit_button(
                            "❌ Cancel",
                            use_container_width=True
                        )

                    if save_button:

                        if edit_amount <= 0:

                            st.error(
                                "Amount must be greater than ₹0."
                            )

                        elif not edit_description.strip():

                            st.error(
                                "Description cannot be empty."
                            )

                        else:

                            success = update_expense(
                                expense["id"],
                                edit_category,
                                edit_amount,
                                edit_date,
                                edit_description,
                                edit_payment
                            )

                            if success:

                                st.session_state.editing_id = None

                                st.success(
                                    "✅ Expense updated successfully!"
                                )

                                st.rerun()

                            else:

                                st.error(
                                    "Could not update expense."
                                )

                    if cancel_button:

                        st.session_state.editing_id = None

                        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    '💰 Expense Tracker'
    '<br><br>'
    'Built with Python + Streamlit + JSON'
    '<br>'
    'Developed by <b>Sheik Mohammad Riyaaz</b>'
    '</div>',
    unsafe_allow_html=True
)