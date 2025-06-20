# HackMap Haifa

#### Video Demo: [https://youtu.be/uxGDpDOnSQk](https://youtu.be/uxGDpDOnSQk)

---

## תיאור כללי / Overview

HackMap Haifa הוא יישום ווב קוד-פתוח שמרכז ומשתף אירועי הייטק בחיפה והקריות על-גבי מפה אינטראקטיבית.
**האתגר:** האקתונים, Meetups וכנסים מפורסמים במקורות שונים (Facebook, Meetup, Eventbrite) וקשה לעקוב אחריהם.
**הפתרון:** אפליקציית **Flask + Leaflet** שמאפשרת לכל משתמש להוסיף אירוע בלחיצה, לצפות בכל האירועים בזמן-אמת ולהוריד אותם כ-JSON.

---

## תכונות עיקריות / Key Features

| Feature                 | Details                                                                   |
| ----------------------- | ------------------------------------------------------------------------- |
| **Interactive Map**     | Leaflet + OpenStreetMap, ממוקדת ‎32.79 °N 34.98 °E; סמני-מיקום עם pop-up. |
| **REST API**            | `GET /api/events` מחזיר JSON; `POST /api/events` מוסיף אירוע ומחזיר 201.  |
| **SQLite DB**           | טבלה יחידה `events` (title, description, category, date, lat, lng).       |
| **GPS Auto-Locate**     | בעת הוספה, הדפדפן מציע להשתמש במיקום הנוכחי (HTML5 Geolocation).          |
| **CORS Enabled**        | flask-cors מאפשר צריכה מאפליקציות Mobile או דומיינים אחרים.               |
| **Zero-Config Install** | `python init_db.py` יוצר DB; אין תלות Docker או ענן חובה.                 |

---

## קבצים ותיקיות / File Structure

| Path                       | Purpose                                           |
| -------------------------- | ------------------------------------------------- |
| `app.py`                   | קוד Flask — נתיבים API + תבנית `/map`.            |
| `schema.sql`               | סכמה ל-DB, ניתנת להרצה ידנית או ע"י `init_db.py`. |
| `init_db.py`               | יצירת `hackmap.db` והזרעת אירוע-דוגמה.            |
| `templates/index.html`     | דף המפה + טופס “הוסף אירוע” (Jinja2).             |
| `static/main.js`           | JavaScript — Leaflet, fetch, וולידציה בצד-לקוח.   |
| `requirements.txt`         | Flask 3.1, flask-cors 6.0, pytest וכו׳.           |
| `.github/workflows/ci.yml` | GitHub Actions להרצת בדיקות ו-flake8.             |

---

## התקנה מהירה / Quick Start

```bash
git clone https://github.com/oren40/hackmap-haifa.git
cd hackmap-haifa/project
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python init_db.py          # יוצר hackmap.db
flask --app app run        # http://127.0.0.1:5000/map
```

---

## Architecture / מבט מערכתי

HackMap Haifa מחולק לשלוש שכבות:

| Layer            | Tech                                | Responsibility                                          |
| ---------------- | ----------------------------------- | ------------------------------------------------------- |
| **Presentation** | HTML + TailwindCSS CDN + Leaflet.js | UI, מפה, טופס, toast להודעות-שגיאה.                     |
| **API**          | Flask 3.1 (Python 3.12)             | Endpoints, ולידציה, החזרת JSON, CORS.                   |
| **Data**         | SQLite 3                            | אחסון אירועים; כל שאילתה עם parameter-binding נגד SQLi. |

### Database Schema

```sql
CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  category TEXT CHECK(category IN ('Hackathon','Meetup','Conf')),
  date TEXT NOT NULL,      -- ISO 8601 UTC
  lat  REAL NOT NULL,
  lng  REAL NOT NULL
);
```

### Route Map

| Method | Path          | Purpose                |
| ------ | ------------- | ---------------------- |
| GET    | `/map`        | HTML + JS (דף ראשי)    |
| GET    | `/api/events` | החזרת אירועים ב-JSON   |
| POST   | `/api/events` | הוספת אירוע חדש        |
| GET    | `/healthz`    | בדיקת 200 OK לדוקר/ענן |

---

## Development Workflow

1. **Lint & Format** – `pre-commit` מריץ black + flake8.
2. **Unit Tests** – `pytest test_api.py` בודק 200/400 ותוכן JSON.
3. **CI** – GitHub Actions מריץ Python 3.12 על Ubuntu-latest.
4. **CD (optional)** – Render.com Auto-Deploy בעת push ל-`main`.

---

## Deployment Notes

* **Render.com** – קובץ `render.yaml` מגדיר build command ו-`gunicorn app:app`.
* **Fly.io** – `fly.toml` קובע ‎8080 + health check ל-`/healthz`.
* ניתן להריץ Docker מקומי:

  ```bash
  docker build -t hackmap .
  docker run -p 5000:5000 hackmap
  ```

---

## Design Notes / החלטות ארכיטקטורה

* **Flask + Jinja** נבחר לשילוב API + SSR ללא React/Bundler — מאפשר קוד קצר וברור.
* **Leaflet CDN-only** במקום Google Maps → ללא API-key וקל לעטוף באנגלית/עברית.
* **Single-table SQLite** מספיק ל-MVP; מעבר עתידי ל-PostgreSQL יחייב שינוי connection-string יחיד.
* ולידציה בסיסית מתבצעת בצד-לקוח; בצד-שרת חוסר שדות מחזיר `400 Bad Request`.
* קוד נגיש (labels, role="alert") כדי לתמוך ב-screen readers.

---

## Testing Strategy

| Tool               | Coverage                              |
| ------------------ | ------------------------------------- |
| **pytest**         | בדיקות יחידה ל-API, כולל Edge cases.  |
| **Playwright**     | בדיקות E2E: הוספת אירוע → הופעה במפה. |
| **flake8 / black** | אחידות סגנון, PEP-8.                  |

---

## AI Disclosure

חלקי קוד (שורות 24-55 ב-`app.py`, שאילתת `INSERT` ב-`schema.sql`) נוצרו עם ChatGPT-4o, ולאחר מכן נערכו ונבדקו ידנית.

---

## Future Work

1. OAuth (Google) לשיוך אירועים למשתמשים.
2. סינון/חיפוש לפי תאריך וקטגוריה + pagination.
3. דיפלוי קבוע ל-Render/Fly.io.
4. התראות-מייל 24 ש׳ לפני תחילת אירוע.
5. Marker-Clustering כשה-DB יגדל ל-500+ רשומות.

---

## Known Limitations

* אין אימות משתמשים — כל אחד יכול להוסיף/למחוק.
* `/api/events` מחזיר את כל הרשומות; paging עתידי.
* Rate-limit מתבצע רק ברמת reverse-proxy (לא באפליקציה).

---

## Credits

* Leaflet © OpenStreetMap contributors
* CS50x 2025 staff — הנחיה ומשוב

---

## License

Released under the **MIT License**.
