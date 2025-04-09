# 🧑‍💻 Flet Login System

A simple login and registration system built using [Flet](https://flet.dev/) and SQLite. The app features user authentication, account creation, and basic password hashing with SHA-256. It uses a dark mode interface and includes date picker support for selecting birth dates.

---

## 🚀 Features

- User registration with:
  - Full name
  - Email
  - Birth date
  - Username
  - Password confirmation
- Secure password storage using SHA-256 hashing
- Login authentication
- Error and success messages
- Modern UI built with Flet
- SQLite-based local database
- Dark mode theme

---

## 📦 Requirements

- Python 3.8+
- [Flet](https://pypi.org/project/flet/)

Install dependencies:

```bash
pip install flet
```

---

## 🛠️ How to Run

```bash
python app.py
```

> The database (`login_db.sqlite`) will be created automatically on first run.

---

## 📁 File Structure

```
.
├── app.py          # Main application code
├── login_db.sqlite # SQLite DB (auto-generated)
└── README.md       # Project documentation
```

---

## 🔐 Security Note

This project uses SHA-256 for basic password hashing. For production systems, it's recommended to use stronger hashing algorithms like bcrypt or Argon2, and implement additional security features like salting, rate limiting, and email verification.

---

## ✨ Screenshots

![Login UI](https://github.com/user-attachments/assets/5d84ac20-c0b0-4e0b-965f-ad35fc9e9214)

![Register UI](https://github.com/user-attachments/assets/94ecec8d-f151-46ea-965d-ee96c0c60f35)

![Calendar](https://github.com/user-attachments/assets/ed16b935-c89f-4aba-ae93-cf8416b81775)

---

## 📌 Todo

- Password recovery system
- Email verification
- Password strength checker
- Better input validation and sanitization
- Admin panel

---

## 📃 License

MIT License
