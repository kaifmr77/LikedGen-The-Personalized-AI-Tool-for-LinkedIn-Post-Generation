import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
from io import BytesIO
from docx import Document
from reportlab.pdfgen import canvas
import random
import pandas as pd
import os
from datetime import datetime

# ---------- Options ----------
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
tone_options = ["Professional", "Friendly", "Motivational", "Casual"]

# ---------- Session State ----------
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_post" not in st.session_state:
    st.session_state.selected_post = None


# ---------- Helpers ----------
def export_docx(text):
    doc = Document()
    doc.add_paragraph(text)
    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf


def export_pdf(text):
    buf = BytesIO()
    c = canvas.Canvas(buf)
    text_object = c.beginText(40, 800)
    for line in text.split("\n"):
        text_object.textLine(line)
    c.drawText(text_object)
    c.showPage()
    c.save()
    buf.seek(0)
    return buf


def generate_hashtags(tag):
    base = {
        "Job Search": ["#JobSearch", "#CareerGrowth", "#ResumeTips"],
        "Motivation": ["#Inspiration", "#NeverGiveUp", "#PositiveVibes"],
        "Mental Health": ["#MentalHealth", "#WellBeing", "#SelfCare"],
    }
    return " ".join(base.get(tag, ["#LinkedIn", "#Networking", "#Growth"]))


def suggest_cta():
    ctas = [
        "💭 What are your thoughts? Share in comments!",
        "👇 Have you faced this? Let’s discuss below.",
        "🚀 Tag someone who needs to read this!",
        "✨ Share your perspective in the comments.",
    ]
    return random.choice(ctas)


# ---------- Main App ----------
def main():
    st.subheader("💡 LinkedGen - Personalized AI Tool")

    col1, col2, col3, col4 = st.columns(4)
    fs = FewShotPosts()
    tags = fs.get_tags()

    def clear_preview():
        st.session_state.selected_post = None

    # Dropdowns
    with col1:
        selected_tag = st.selectbox("📌 Topic", options=tags, on_change=clear_preview, key="tag")
    with col2:
        selected_length = st.selectbox("📏 Length", options=length_options, on_change=clear_preview, key="length")
    with col3:
        selected_language = st.selectbox("🌐 Language", options=language_options, on_change=clear_preview, key="lang")
    with col4:
        selected_tone = st.selectbox("🎭 Tone", options=tone_options, on_change=clear_preview, key="tone")

    # -------- Reset All --------
    if st.button("♻️ Reset All"):
        st.session_state.clear()
        st.rerun()

    # -------- Generate Single Post --------
    if st.button("✨ Generate Post"):
        raw_post = generate_post(selected_length, selected_language, selected_tag, selected_tone)
        hashtags = generate_hashtags(selected_tag)
        cta = suggest_cta()
        post = f"[Tone: {selected_tone}] | [Language: {selected_language}]\n\n{raw_post}\n\n{hashtags}\n\n{cta}"

        st.session_state.history.insert(0, post)
        if len(st.session_state.history) > 20:
            st.session_state.history.pop()

        st.session_state.selected_post = post

    # -------- Show Selected Post --------
    if st.session_state.selected_post:
        st.markdown("### 📢 Post Preview")
        st.markdown(
            f"<div style='border:1px solid #ccc; padding:15px; border-radius:10px; background:black; color:white;'>{st.session_state.selected_post}</div>",
            unsafe_allow_html=True,
        )

        st.info(
            f"Word count: {len(st.session_state.selected_post.split())} | Character count: {len(st.session_state.selected_post)}")

        edited_post = st.text_area("✍️ Edit Your Post", st.session_state.selected_post, height=200)

        colA, colB, colC, colD = st.columns(4)
        with colA:
            st.download_button("⬇️ TXT", edited_post, file_name="linkedin_post.txt")
        with colB:
            st.download_button("⬇️ DOCX", export_docx(edited_post), file_name="linkedin_post.docx")
        with colC:
            st.download_button("⬇️ PDF", export_pdf(edited_post), file_name="linkedin_post.pdf")
        with colD:
            schedule_time = st.text_input("⏰ Schedule (YYYY-MM-DD HH:MM)", placeholder="2025-08-26 14:30")
            if st.button("📅 Save Schedule"):
                if schedule_time.strip():
                    schedule_entry = {
                        "timestamp": schedule_time,
                        "post": edited_post
                    }
                    schedule_file = "scheduled_posts.csv"
                    if os.path.exists(schedule_file):
                        df = pd.read_csv(schedule_file)
                        df = pd.concat([df, pd.DataFrame([schedule_entry])], ignore_index=True)
                    else:
                        df = pd.DataFrame([schedule_entry])
                    df.to_csv(schedule_file, index=False)
                    st.success(f"✅ Post scheduled for {schedule_time}")

    # -------- Generate Multiple Variations --------
    if st.button("🔄 Generate 3 Variations"):
        st.subheader("Multiple Variations")
        for i in range(1, 4):
            post = generate_post(selected_length, selected_language, selected_tag, selected_tone)
            hashtags = generate_hashtags(selected_tag)
            st.markdown(f"**Variation {i}:**")
            st.write(post + "\n\n" + hashtags + "\n\n" + suggest_cta())
            st.divider()

    # -------- Sidebar (History + Credits + Feedback + Schedule) --------
    with st.sidebar:
        st.subheader("🕒 Recent Posts")

        search_query = st.text_input("🔍 Search history")
        filter_tone = st.selectbox("🎭 Filter by Tone", ["All"] + tone_options)
        filter_lang = st.selectbox("🌐 Filter by Language", ["All"] + language_options)

        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.session_state.selected_post = None
            st.success("History cleared!")

        if st.session_state.history:
            all_posts = "\n\n---\n\n".join(st.session_state.history)
            st.download_button("⬇️ Export All (TXT)", all_posts, file_name="all_posts.txt")
            st.download_button("⬇️ Export All (DOCX)", export_docx(all_posts), file_name="all_posts.docx")
            st.download_button("⬇️ Export All (PDF)", export_pdf(all_posts), file_name="all_posts.pdf")
            st.markdown("---")

            for i, hpost in enumerate(st.session_state.history):
                if search_query and search_query.lower() not in hpost.lower():
                    continue
                if filter_tone != "All" and f"[Tone: {filter_tone}]" not in hpost:
                    continue
                if filter_lang != "All" and f"[Language: {filter_lang}]" not in hpost:
                    continue

                if st.button(f"View Post {i + 1}"):
                    st.session_state.selected_post = hpost

                if st.checkbox(f"⭐ Pin Post {i + 1}", key=f"pin_{i}"):
                    st.session_state.history.insert(0, st.session_state.history.pop(i))
        else:
            st.info("No history yet.")

        # --- Developer Credits ---
        st.markdown("---")
        st.subheader("👨‍💻 Developer Credits")
        st.markdown("""
        **Developed by:** Mohammed Kaif  
        📧 Email: Kaifmohammed167@gmail.com  
        🔗 LinkedIn: [https://www.linkedin.com/in/kaifmr7/]    
        📱 Contact: +91-9663222714 
        """)

        # --- Feedback Section ---
        st.markdown("---")
        st.subheader("💬 Feedback")

        user_name = st.text_input("Your Name (optional)", placeholder="Enter your name")
        feedback_text = st.text_area("Share your feedback:", placeholder="Type your feedback here...")
        rating = st.slider("Rate this app (1 = Poor, 5 = Excellent)", 1, 5, 3)

        if st.button("Submit Feedback"):
            if feedback_text.strip():
                feedback_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user": user_name if user_name else "Anonymous",
                    "feedback": feedback_text,
                    "rating": rating
                }
                feedback_file = "feedback.csv"
                if os.path.exists(feedback_file):
                    df = pd.read_csv(feedback_file)
                    df = pd.concat([df, pd.DataFrame([feedback_entry])], ignore_index=True)
                else:
                    df = pd.DataFrame([feedback_entry])
                df.to_csv(feedback_file, index=False)
                st.success("✅ Thank you for your feedback! Saved successfully.")
            else:
                st.warning("⚠️ Please enter feedback before submitting.")

        feedback_file = "feedback.csv"
        if os.path.exists(feedback_file):
            st.markdown("### 📝 Previous Feedback")
            df = pd.read_csv(feedback_file)
            for _, row in df.tail(5).iterrows():
                st.write(f"🕒 {row['timestamp']} | 👤 {row['user']} | ⭐ {row['rating']}/5")
                st.caption(row['feedback'])

        # --- Scheduled Posts Section ---
        st.markdown("---")
        st.subheader("📅 Scheduled Posts")

        schedule_file = "scheduled_posts.csv"
        if os.path.exists(schedule_file):
            df = pd.read_csv(schedule_file)
            if not df.empty:
                for idx, row in df.iterrows():
                    st.write(f"🕒 {row['timestamp']}")
                    st.caption(row['post'][:150] + "..." if len(row['post']) > 150 else row['post'])

                    if st.button(f"❌ Delete {row['timestamp']}", key=f"del_{idx}"):
                        df = df.drop(idx).reset_index(drop=True)
                        df.to_csv(schedule_file, index=False)
                        st.success("🗑️ Scheduled post deleted.")
                        st.rerun()
            else:
                st.info("No scheduled posts yet.")
        else:
            st.info("No scheduled posts yet.")


# Run App
if __name__ == "__main__":
    main()
