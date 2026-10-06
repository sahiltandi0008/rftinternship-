import streamlit as st
import pandas as pd
import re
import io
from datetime import datetime
import pdfplumber

st.set_page_config(
    page_title="Automated Invoice Processing System",
    layout="wide"
)

st.title("🧾 Automated Invoice Processing System")

uploaded_files = st.file_uploader(
    "Upload Invoice CSV or PDF Files",
    type=["csv", "pdf"],
    accept_multiple_files=True
)

today = datetime.today().date()

results = []

if uploaded_files:

    for file in uploaded_files:

        text = ""

        if file.name.lower().endswith(".pdf"):

            file.seek(0)

            with pdfplumber.open(file) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

        elif file.name.lower().endswith(".csv"):

            file.seek(0)

            csv_data = pd.read_csv(file)

            text = csv_data.to_string(index=False)

        invoice_match = re.search(
            r"(?:Invoice Number|Invoice No|Invoice #|Invoice)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
            text,
            re.IGNORECASE
        )

        invoice_number = (
            invoice_match.group(1)
            if invoice_match
            else "Not Found"
        )

        customer_match = re.search(
            r"(?:Customer Name|Customer|Bill To)\s*[:\-]?\s*(.+)",
            text,
            re.IGNORECASE
        )

        customer_name = (
            customer_match.group(1).strip()
            if customer_match
            else "Not Found"
        )

        email_match = re.search(
            r"[\w\.-]+@[\w\.-]+\.\w+",
            text
        )

        customer_email = (
            email_match.group(0)
            if email_match
            else "Not Found"
        )

        phone_match = re.search(
            r"(?:Phone|Mobile|Contact)\s*[:\-]?\s*(\+?\d[\d\s\-]{8,})",
            text,
            re.IGNORECASE
        )

        customer_phone = (
            phone_match.group(1).strip()
            if phone_match
            else "Not Found"
        )

        date_match = re.search(
            r"(?:Invoice Date|Date)\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2})",
            text,
            re.IGNORECASE
        )

        invoice_date = (
            date_match.group(1)
            if date_match
            else "Not Found"
        )

        parsed_date = pd.to_datetime(
            invoice_date,
            errors="coerce"
        )

        due_date_match = re.search(
            r"(?:Due Date|Payment Due)\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2})",
            text,
            re.IGNORECASE
        )

        if due_date_match:

            due_date = pd.to_datetime(
                due_date_match.group(1),
                errors="coerce"
            )

        else:

            due_date = pd.NaT

        total_match = re.search(
            r"(?:Grand Total|Total Amount|Invoice Total|Total)\s*[:\-]?\s*(?:₹|\$|Rs\.?)?\s*([\d,]+(?:\.\d{1,2})?)",
            text,
            re.IGNORECASE
        )

        if total_match:

            total_amount = float(
                total_match.group(1).replace(",", "")
            )

        else:

            amounts = re.findall(
                r"(?:₹|\$|Rs\.?)\s*([\d,]+(?:\.\d{1,2})?)",
                text,
                re.IGNORECASE
            )

            if amounts:

                total_amount = sum(
                    float(x.replace(",", ""))
                    for x in amounts
                )

            else:

                total_amount = 0.0

        item_matches = re.findall(
            r"([A-Za-z][A-Za-z0-9\s\-]{2,})\s+(?:₹|\$|Rs\.?)?\s*([\d,]+(?:\.\d{1,2})?)",
            text
        )

        items = []

        for item, price in item_matches:

            item = item.strip()

            if len(item) > 2:

                items.append(
                    f"{item}: ₹{float(price.replace(',', '')):.2f}"
                )

        item_details = "; ".join(items)

        if pd.notna(due_date):

            overdue = due_date.date() < today

        else:

            overdue = False

        results.append({
            "File Name": file.name,
            "Invoice Number": invoice_number,
            "Customer Name": customer_name,
            "Customer Email": customer_email,
            "Customer Phone": customer_phone,
            "Invoice Date": (
                parsed_date.strftime("%Y-%m-%d")
                if pd.notna(parsed_date)
                else "Not Found"
            ),
            "Due Date": (
                due_date.strftime("%Y-%m-%d")
                if pd.notna(due_date)
                else "Not Found"
            ),
            "Items & Prices": item_details,
            "Total Amount": total_amount,
            "Overdue": "Yes" if overdue else "No"
        })

if results:

    report = pd.DataFrame(results)

    st.subheader("📊 Invoice Summary")

    total_invoices = len(report)

    total_amount = report["Total Amount"].sum()

    overdue_invoices = (
        report["Overdue"] == "Yes"
    ).sum()

    overdue_amount = report.loc[
        report["Overdue"] == "Yes",
        "Total Amount"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Invoices",
        total_invoices
    )

    col2.metric(
        "Total Invoice Amount",
        f"₹{total_amount:,.2f}"
    )

    col3.metric(
        "Overdue Invoices",
        overdue_invoices
    )

    col4.metric(
        "Overdue Amount",
        f"₹{overdue_amount:,.2f}"
    )

    st.subheader("🧾 Consolidated Invoice Report")

    st.dataframe(
        report,
        use_container_width=True
    )

    st.subheader("🔎 Invoice Search & Filters")

    search = st.text_input(
        "Search Invoice Number or Customer"
    )

    status_filter = st.multiselect(
        "Invoice Status",
        ["Yes", "No"],
        default=["Yes", "No"]
    )

    filtered_report = report[
        report["Overdue"].isin(status_filter)
    ]

    if search:

        filtered_report = filtered_report[
            filtered_report["Invoice Number"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
            |
            filtered_report["Customer Name"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        filtered_report,
        use_container_width=True
    )

    st.subheader("⚠️ Overdue Invoices")

    overdue_report = report[
        report["Overdue"] == "Yes"
    ]

    if len(overdue_report) > 0:

        st.error(
            f"{len(overdue_report)} overdue invoice(s) found."
        )

        st.dataframe(
            overdue_report,
            use_container_width=True
        )

    else:

        st.success(
            "No overdue invoices found."
        )

    st.subheader("📈 Invoice Amount Analysis")

    amount_data = report[
        ["Invoice Number", "Total Amount"]
    ].copy()

    amount_data = amount_data.set_index(
        "Invoice Number"
    )

    st.bar_chart(amount_data)

    st.subheader("📋 Automated Summary Report")

    summary = pd.DataFrame({
        "Metric": [
            "Total Invoices",
            "Total Invoice Amount",
            "Overdue Invoices",
            "Overdue Amount",
            "Paid/Non-Overdue Invoices",
            "Average Invoice Amount"
        ],
        "Value": [
            total_invoices,
            total_amount,
            overdue_invoices,
            overdue_amount,
            total_invoices - overdue_invoices,
            report["Total Amount"].mean()
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True
    )

    st.subheader("📥 Export Final Report")

    csv_report = report.to_csv(
        index=False
    )

    st.download_button(
        label="Download Consolidated Invoice Report",
        data=csv_report,
        file_name="consolidated_invoice_report.csv",
        mime="text/csv"
    )

    summary_csv = summary.to_csv(
        index=False
    )

    st.download_button(
        label="Download Summary Report",
        data=summary_csv,
        file_name="invoice_summary_report.csv",
        mime="text/csv"
    )

else:

    st.info(
        "Upload one or more CSV/PDF invoice files to begin."
    )

