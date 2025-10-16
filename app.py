import streamlit as st
import pandas as pd
import datetime
import io
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics

# إعداد صفحة Streamlit
st.set_page_config(page_title="تقرير الطلبات", layout="wide")

st.title("📦 إنشاء تقرير الطلبات (PDF)")

uploaded_file = st.file_uploader("📤 ارفع ملف Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📋 البيانات:")
    st.dataframe(df)

    file_name = st.text_input("✏️ اسم ملف PDF", "تقرير الطلبات")

    if st.button("📄 إنشاء PDF"):
        buffer = io.BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

        elements = []

        # إعداد العنوان
        style_title = ParagraphStyle(
            name="Title",
            fontName="Helvetica-Bold",
            fontSize=20,
            alignment=1,
            textColor=colors.HexColor("#64B5F6")
        )
        elements.append(Paragraph(get_display(arabic_reshaper.reshape("تقرير الطلبات")), style_title))
        elements.append(Spacer(1, 20))

        # تحضير الجدول
        data = [list(df.columns)] + df.values.tolist()

        # تحويل النصوص العربية
        reshaped_data = []
        for row in data:
            reshaped_row = []
            for cell in row:
                if isinstance(cell, str):
                    reshaped_row.append(get_display(arabic_reshaper.reshape(cell)))
                else:
                    reshaped_row.append(cell)
            reshaped_data.append(reshaped_row)

        # إنشاء الجدول
        table = Table(reshaped_data, repeatRows=1)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#64B5F6")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ]))

        elements.append(table)
        pdf.build(elements)

        st.success("✅ تم إنشاء ملف PDF بنجاح!")
        st.download_button(
            label="⬇️ تحميل PDF",
            data=buffer.getvalue(),
            file_name=f"{file_name}.pdf",
            mime="application/pdf"
        )
