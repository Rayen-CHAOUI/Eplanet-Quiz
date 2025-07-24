# ProLingo

 An English language platform built with [Flet](https://flet.dev/) and `SQLite3`. Where users can register, log in, and take quizzes with multimedia questions **(text, image, and audio)**. Admins can manage users and questions via a Dashboard, Users also have access to various learning course pages such as **Grammar**, **Vocabulary**, **Speaking**, **Listening**, and **Exercises**.

--- 

## Screenshots

- Login and signup pages.
- User dashboard with quiz and learning buttons.
- Interactive quiz screen with question navigation.
- Grammar, Vocabulary, Speaking, Listening, and Exercise course pages.
- Final result page showing detailed performance.
- Admin dashboard to manage users and import questions.
- Profile page to edit user's info.

--- 

## Features

### User Features
- Users stored in `backend/eplanet_users.db/user`.
- User registration and login with **ID** and **password**.
- Multiple levels **(Elementary, Pre-intermediate, Intermediate, Upper-intermediate, Advanced)**.
- Change **password**, **level**, **username**.
- Access to **course pages**:
    - Grammar.
    - Vocabulary.
    - Speaking.
    - Listening.
    - Exercises.
- Real-time quiz interaction (with **audio** and **image support**).
- Ability to **select/change** answers before clicking "Next".
- **Final result page** with:
    - Total score.
    - Detailed table showing correct and incorrect answers.

### Admin Features
- Admins stored in `backend/eplanet_users.db/admin`
- Admin login via session.
- View registered users with **performance stats**.
- Add questions manually or import from **JSON/Excel**.
- Upload question assets **(images/audio)**.
- Edit user's info (**password**, **level**, **username**).
- Add new users and admins.

---

### Quiz Logic
- Questions stored in `backend/quiz_questions.db`.
- Assets stored in `assets/images/` and `assets/audio/`.
- Correct/wrong answers saved per user in `eplanet_users.db/user`.

---

### Lessons Logic
- Lessons stored in `backend/lessons/grammar.db`,  `backend/lessons/vocabulary.db`.. etc
- Assets stored in `assets/images/` and `assets/audio/`.
- Correct/wrong answers for the exercises displayed in **real-time**.

---

## Technologies Used

- **Python** : Core programming language.
- **Flet** : UI framework for building apps with Flutter-like widgets in Python.
-  **SQLite3** : Lightweight embedded database. 
- **JSON / Excel** : Question import support.
- **Reportlab** : Extract result into **PDF file**.

---

## Installation 

1. Clone the repo : 

```bash
   git clone https://github.com/Rayen-CHAOUI/ProLingo.git
```
```bash
    cd ProLingo
```

2. install dependencies : 

```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install flet[all] 
    pip3 install reportlab
```

3. Run the app : 

```bash
    python3 main.py
```

---

##  Upcoming Improvements

- Timer per question.
- Question categories (Grammar, Listening, etc.). ---> **DONE**
- User statistics and progress tracking. ---> **DONE**
- Export results to PDF. ---> **DONE**

--- 

## License
This project is under the MIT License.

--- 

## Contributing
Pull requests and ideas are welcome!

---

## Contact
Open an issue or contact me via GitHub or Instagram if you have questions or suggestions.

---

## Author
CHAOUI Rayen.
---