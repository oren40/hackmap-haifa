# HackMap Haifa
#### Video Demo: https://youtu.be/uxGDpDOnSQk

## תיאור כללי / Overview
HackMap Haifa הוא יישום ווב קוד-פתוח שמרכז ומשתף אירועי הייטק בחיפה והקריות על-גבי מפה אינטראקטיבית.  
**האתגר:** האקתונים, Meetups וכנסים מתפרסמים במקורות שונים (Facebook, Meetup, Eventbrite) וקשה לעקוב אחריהם.  
**הפתרון:** אפליקציית Flask + Leaflet שמאפשרת לכל משתמש להוסיף אירוע בלחיצה, לצפות בכל האירועים בזמן-אמת ולהוריד אותם כ-JSON

## תכונות עיקריות / Key Features
* Interactive Map – Leaflet + OpenStreetMap, ממוקדת 32.79°N 34.98°E  
* REST API – GET /api/events מחזיר את כל האירועים; POST /api/events מוסיף חדש  
* SQLite DB – טבלה בודדת events (title, description, category, date, lat, lng)  
* GPS Auto-Locate – הדפדפן מציע להשתמש במיקום הנוכחי בעת הוספת אירוע  
* CORS Enabled – ניתן לשלב אתר חיצוני או Mobile App בקלות  

## קבצים ותיקיות / File Structure
app.py – קוד Flask – API routes + תבנית /map  
schema.sql – סכמה לטבלה events  
init_db.py – סקריפט חד-פעמי ליצירת hackmap.db  
templates/index.html – דף המפה + טופס “הוסף אירוע”  
static/main.js – JavaScript – Leaflet, fetch, ולידציה  
requirements.txt – Flask + flask-cors (תלויות Python)

## התקנה מהירה / Quick Start
git clone https://github.com/oren40/hackmap-haifa.git  
cd hackmap-haifa/project  
python3 -m venv venv && source venv/bin/activate  
pip install -r requirements.txt  
python init_db.py            # יוצר hackmap.db  
flask --app app run          # http://127.0.0.1:5000/map

## Design Notes / ארכיטקטורה וקבלת החלטות
- Flask + Jinja נבחר לשילוב מהיר של API ותבניות, בלי React/Bundler  
- Leaflet (CDN-only) – קל-משקל, ללא build-step, אידיאלי לפרויקט לימודי  
- Single-table SQLite מספיק ל-MVP; אם נוסיף משתמשים/תגובות נעבור ל-PostgreSQL  
- ולידציה בסיסית בצד-לקוח; בצד-שרת חסרים שדות מחזירים 400  
- נעזרתי ב-ChatGPT לחלקי קוד, לאחר מכן ליטשתי ידנית  

## AI Disclosure
חלקי קוד (שורות 24-55 ב-app.py, שאילתת INSERT ב-schema.sql) נוצרו עם ChatGPT-4o ולאחר מכן עברו בדיקה ושיפור ידניים.

## Future Work
1. הוספת OAuth (Google) לשיוך אירועים למשתמשים  
2. פילטר חיפוש לפי תאריכים וקטגוריות  
3. דיפלוי ל-Render / Fly.io לשימוש ללא התקנה  
4. התראות-מייל 24 שעות לפני אירוע  

## Credits
Leaflet © OpenStreetMap contributors  
CS50x 2025 staff – הנחיה ומשוב  

## License
Released under the MIT License.

