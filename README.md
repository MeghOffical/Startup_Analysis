# Startup Funding Analysis Web App

A Streamlit-based interactive web application for analyzing startup funding data, built in Python. 
Users can explore overall funding trends, dive into individual startup or investor details, and visualize data through charts and heatmaps.

🔍 Project Overview

This project provides a user-friendly dashboard to analyze startup funding information, including:

* **Overall Analysis**: Key metrics (total, max, average funding, number of funded startups), month-over-month trends, top sectors, funding types, city-wise funding, top startups & investors, and a funding heatmap.
* **Startup Details**: Recent investments, biggest investors, industry and city breakdowns, year-over-year growth, and similar startups by domain.
* **Investor Details**: Recent investments, top funded startups, industry and stage breakdowns, year-over-year growth, and similar investors by domain.

The app leverages Streamlit for interactivity and Python libraries (`pandas`, `matplotlib`, `seaborn`) for data processing and visualization.



 📁 Repository Structure

```bash
├── app.py             # Main Streamlit application
├── finalized.csv      # Cleaned startup funding dataset (CSV)
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```


🚀 Getting Started

### Prerequisites

* Python 3.7 or higher
* Git (for cloning the repository)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/startup-funding-analysis.git
   cd startup-funding-analysis
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Place the dataset**

   Ensure `finalized.csv` is in the project root. It should contain the following columns
   * `date`, `startup`, `industry`, `subvertical`, `city`, `investors`, `round`, `amount`, `year`, `month`


### Running the App
```bash
streamlit run app.py
```


---

🛠️ Features

* **Interactive Sidebar**: Choose between Overall Analysis, Startups, or Investors.
* **Dynamic Visualizations**: Bar charts, pie charts, line plots, and heatmaps.
* **Similarity Functions**: Find similar startups or investors by domain (industry/subvertical).
* **Metrics Dashboard**: Key funding metrics displayed as Streamlit metrics.
* **Customizable Filters**: Select startups or investors from dropdown lists.

---


🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add YourFeature"`)
4. Push to your branch (`git push origin feature/YourFeature`)
5. Open a Pull Request


✉️ Contact

Developed by Megh Bavarva

* Email: [bavarvamegh3139@gmail.com](mailto:bavarvamegh3139@gmail.com)
* LinkedIn: [https://www.linkedin.com/in/megh-bavarva-588b78284]

Feel free to open issues or reach out for questions and collaboration!
