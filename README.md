# 3xample Connectivity Analyzer

An **intelligent internet connectivity analyzer** powered by **Machine Learning**.  
Unlike traditional speed tests that only give raw numbers, **3xample** provides:  

- 📊 Real-time speed, latency, jitter, and packet loss measurements  
- 🤖 ML-based predictions of connection quality (*Excellent / Good / Poor*)  
- 💡 Actionable recommendations to improve your internet performance  

Hosted at **[3xample.ca](https://3xample.ca)** (coming soon).  

---

## 🚀 Features

- **Speed Test Core**
  - Download / Upload speeds
  - Latency (ping)
  - Jitter & packet loss

- **Machine Learning Intelligence**
  - Predicts connection quality from test data
  - Detects anomalies & instability
  - Explains likely root causes (Wi-Fi, ISP congestion, device issues)

- **Smart Recommendations**
  - Practical suggestions like *“Try switching to 5GHz Wi-Fi”* or *“Your ISP may be throttling upload speeds.”*

- **Clean Dashboard**
  - Modern React frontend
  - Historical results & trends (Phase 3)

---

## 🛠️ Tech Stack

- **Frontend:** React + Tailwind + Recharts  
- **Backend:** FastAPI (Python)  
- **ML Models:** Scikit-learn (Random Forest / XGBoost)  
- **Database:** Oracle Autonomous DB (Always Free)  
- **Cloud Hosting:** Oracle Cloud Infrastructure (OCI Free Tier)  
- **Domain:** [3xample.ca](https://3xample.ca)  

---

## 📅 Roadmap

### Phase 1 – MVP (Baseline Speed Test) ✅
- [ ] Setup FastAPI backend with `/test` endpoint (speedtest-cli)  
- [ ] Simple React frontend to display results  
- [ ] Deploy on OCI Free VM  

### Phase 2 – Machine Learning 🔬
- [ ] Collect data (download, upload, ping, jitter, packet loss)  
- [ ] Train ML model to classify connection quality  
- [ ] Add `/analyze` endpoint returning quality + recommendations  

### Phase 3 – Production & Portfolio Polish 🌐
- [ ] User dashboard with history & trends  
- [ ] Authentication (Google / email login)  
- [ ] Docker deployment + HTTPS  
- [ ] Blog section: “3 Examples of How ML Improves Connectivity Tests”  

---

## 📂 Project Structure (planned)

