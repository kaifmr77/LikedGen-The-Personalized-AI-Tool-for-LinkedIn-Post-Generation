
# 🚀 LinkedGen: Personalized AI Tool for LinkedIn Post Generation

LinkedGen is a **Streamlit-based AI tool** that helps users generate professional, engaging, and personalized LinkedIn posts.  
It uses **Groq LLMs** (via `langchain_groq`) with few-shot examples to create posts tailored to user preferences like **topic, length, tone, and language**.  

---

## ✨ Features

- 🎯 **Personalized Posts** – Generate posts based on topic, tone, length, and language (English / Hinglish).  
- 📌 **Smart Hashtags & CTAs** – Auto-generate relevant hashtags and call-to-actions.  
- 📝 **Edit & Export** – Edit posts and export in **TXT, DOCX, or PDF** format.  
- 🔄 **Multiple Variations** – Generate multiple variations of the same post.  
- 🕒 **History & Search** – Maintain and search through generated post history.  
- 📅 **Post Scheduling** – Save and manage scheduled posts.  
- 💬 **Feedback System** – Collect feedback from users with ratings.  
- 👨‍💻 **Developer Credits Section** in the sidebar.  

---

## 🛠️ Tech Stack

- [Python 3.10+](https://www.python.org/)  
- [Streamlit](https://streamlit.io/) – Frontend UI  
- [LangChain](https://www.langchain.com/) – Prompt chaining  
- [Groq LLM](https://groq.com/) – AI text generation  
- [Pandas](https://pandas.pydata.org/) – Data handling  
- [python-docx](https://python-docx.readthedocs.io/) – DOCX export  
- [ReportLab](https://www.reportlab.com/) – PDF export  
- [dotenv](https://pypi.org/project/python-dotenv/) – Environment variable management  

---

## 📂 Project Structure

```

├── few\_shot.py         # Handles loading & filtering few-shot examples
├── llm\_helper.py       # Groq LLM integration with LangChain
├── main.py             # Streamlit app (UI + logic)
├── post\_generator.py   # Post generation logic using LLM
├── preprocess.py       # Preprocessing & metadata extraction for few-shot posts
├── requirements.txt    # Project dependencies
└── data/               # Raw and processed LinkedIn post data (JSON files)

````

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/LinkedGen.git
   cd LinkedGen
````

2. **Create & activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

---

## ▶️ Usage

Run the Streamlit app:

```bash
python -m streamlit run main.py
```

The app will launch at **[http://localhost:8501/](http://localhost:8501/)** in your browser.

---

## 📊 Example Workflow

1. Select **Topic, Length, Tone, and Language**.
2. Click **Generate Post** to get an AI-generated LinkedIn post.
3. Edit, export, or schedule the post directly from the UI.
4. Browse history or generate multiple variations for A/B testing.

---

## 📌 Roadmap

* [ ] Add support for **multi-language posts**.
* [ ] Integrate **real LinkedIn API** for direct posting.
* [ ] Improve scheduling with **cron jobs** or external calendar integration.

---

## 👨‍💻 Developer

**Mohammed Kaif**
📧 Email: [Kaifmohammed167@gmail.com](mailto:Kaifmohammed167@gmail.com)
🔗 LinkedIn: [linkedin.com/in/kaifmr7](https://www.linkedin.com/in/kaifmr7/)
📱 Contact: +91-9663222714

---

## 📝 License

This project is licensed under the **MIT License** – feel free to use, modify, and distribute.

---

⭐ If you find this useful, don’t forget to **star the repo**!


