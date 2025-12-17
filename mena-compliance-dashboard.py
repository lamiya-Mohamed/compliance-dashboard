import streamlit as st
import pandas as pd

# =====================
# Classes
# =====================

class Entity:
    def __init__(self, name, sector, compliance_scores):
        self.entity_name = name
        self.sector = sector
        self.compliance_scores = compliance_scores

    def calculate_total_score(self):
        total = sum(self.compliance_scores)
        count = len(self.compliance_scores)
        return total / count

    def get_compliance_level(self):
        avg_score = self.calculate_total_score()
        if avg_score <= 2:
            return "Low"
        elif avg_score <= 4:
            return "Medium"
        else:
            return "High"

class ComplianceManager:
    def __init__(self):
        self.entities_list = []

    def add_entity(self, entity):
        self.entities_list.append(entity)

    def list_entities(self):
        return [(e.entity_name, e.sector, e.get_compliance_level(), e.calculate_total_score()) for e in self.entities_list]

    def get_dataframe(self):
        # تحويل البيانات لـ DataFrame لعرض البار تشارت
        data = {
            "Entity": [e.entity_name for e in self.entities_list],
            "Score": [e.calculate_total_score() for e in self.entities_list],
            "Level": [e.get_compliance_level() for e in self.entities_list]
        }
        df = pd.DataFrame(data)
        return df

# =====================
# Streamlit App
# =====================

# العنوان بدون PSC
st.title("Risk Management Practitioner Dashboard - MENA")

manager = ComplianceManager()

# بيانات افتراضية (MENA)
default_entities = [
    Entity("وزارة الصحة السعودية", "Health", [4,5,3,4]),
    Entity("أمانة المدينة", "Government", [3,4,2,3]),
    Entity("بنك دبي الإسلامي", "Finance", [5,4,5,4]),
    Entity("شركة الاتصالات الإماراتية", "Telecom", [4,3,4,4]),
    Entity("بنك قطر الوطني", "Finance", [5,4,4,5])
]

for e in default_entities:
    manager.add_entity(e)

# Sidebar لإضافة جهة جديدة
st.sidebar.header("Add New Entity")
name = st.sidebar.text_input("Entity Name")
sector = st.sidebar.text_input("Sector")
scores_input = st.sidebar.text_input("Scores (comma separated, e.g. 4,5,3,4)")

if st.sidebar.button("Add Entity"):
    try:
        scores = [int(s) for s in scores_input.split(",")]
        new_entity = Entity(name, sector, scores)
        manager.add_entity(new_entity)
        st.sidebar.success(f"{name} added successfully!")
    except:
        st.sidebar.error("Please enter valid scores!")

# عرض الجدول
st.subheader("Entities List")
entities_data = manager.list_entities()
for data in entities_data:
    st.write(f"Name: {data[0]}, Sector: {data[1]}, Level: {data[2]}, Score: {data[3]:.1f}")

# عرض البار تشارت باستخدام Streamlit builtin
st.subheader("Compliance Dashboard")

df = manager.get_dataframe()

# عرض البار تشارت بدون matplotlib
st.bar_chart(df.set_index("Entity")["Score"])
