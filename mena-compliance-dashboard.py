import streamlit as st
import matplotlib.pyplot as plt

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

    def plot_dashboard(self):
        names = [e.entity_name for e in self.entities_list]
        scores = [e.calculate_total_score() for e in self.entities_list]
        colors = []

        for e in self.entities_list:
            level = e.get_compliance_level()
            if level == "Low":
                colors.append("red")
            elif level == "Medium":
                colors.append("orange")
            else:
                colors.append("green")

        fig, ax = plt.subplots(figsize=(10,6))
        bars = ax.bar(names, scores, color=colors)
        ax.set_xlabel("Entity Name")
        ax.set_ylabel("Compliance Score")
        ax.set_title("Digital Transformation Compliance Dashboard - MENA")
        plt.xticks(rotation=45)

        # Optional: show score on top of bars
        for bar, score in zip(bars, scores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f'{score:.1f}', ha='center')

        return fig

# =====================
# Streamlit App
# =====================

st.title("PSC Risk Management Practitioner Dashboard - MENA")

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

# عرض البار تشارت باستخدام Matplotlib
st.subheader("Compliance Dashboard")
fig = manager.plot_dashboard()
st.pyplot(fig)
