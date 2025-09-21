#  Weather Data Pipeline

An end-to-end **ETL pipeline** that collects live weather data from the **OpenWeatherMap API**, saves raw JSON files locally, transforms the data into a structured format, and loads it into a **PostgreSQL database** for further analysis.  

##  Features
-  Fetch real-time weather data for multiple cities  
-  Store **raw JSON** data (organized by date & city)  
-  Transform raw JSON → clean tabular format (temperature, humidity, wind speed, etc.)  
-  Load structured data into **PostgreSQL**  
-  Scalable, modular ETL design  

---

## Tech Stack
- **Python** (requests, pandas, sqlalchemy, datetime, json, os)  
- **PostgreSQL** (data storage)  
- **SQLAlchemy** (database connection)  

## 📂 Project Structure

weather-data-pipeline/
│── data/                 # Auto-generated raw data storage
│   └── raw/
│       └── YYYY-MM-DD/
│           └── city.json
│
│── pipeline.py           # Main ETL pipeline script
│── requirements.txt      # Python dependencies
│── README.md             # Documentation


##  ETL Flow Diagram

      +-------------+        +----------------+        +----------------+
      |  OpenWeather| -----> |  Raw JSON Data | -----> | Transform Data |
      |     API     |        |   (Local Disk) |        |   (Clean DF)   |
      +-------------+        +----------------+        +----------------+
                                                          |
                                                          v
                                                  +----------------+
                                                  |  PostgreSQL DB |
                                                  +----------------+

## 🚀 Getting Started

### 1. Clone the repository
### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL

Create a database:

```sql
CREATE DATABASE weather_db;
```

### 4. Update `pipeline.py` with your configs

* Add your **OpenWeatherMap API key**
* Update **PostgreSQL credentials**

### 5. Run the pipeline

```bash
python pipeline.py
```

---

## 📊 Example Output

**Transformed DataFrame before loading to DB:**

| city   | country | weather\_description | temperature\_celsius | humidity\_percent | wind\_speed\_mps | observation\_timestamp |
| ------ | ------- | -------------------- | -------------------- | ----------------- | ---------------- | ---------------------- |
| Dhaka  | BD      | haze                 | 29.5                 | 82                | 2.5              | 2025-09-22 05:30:00    |
| London | GB      | clear sky            | 18.2                 | 61                | 3.1              | 2025-09-22 06:00:00    |

---

## Future Improvements

* Add **Docker + docker-compose** (Postgres + pipeline container)
* Use **Airflow / Prefect** for scheduling
* Build a **Grafana / Tableau dashboard** for visualization
