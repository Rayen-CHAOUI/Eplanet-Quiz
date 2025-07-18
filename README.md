# Eplanet Quiz

**Eplanet Quiz** is an English language quiz platform built with [Flet](https://flet.dev/) and `SQLite3`. Where users can register, log in, and take quizzes with multimedia questions **(text, image, and audio)**. Admins can manage users and questions via a Dashboard, Users also have access to various learning course pages such as **Grammar**, **Vocabulary**, **Speaking**, **Listening**, and **Exercises**.

--- 

## Screenshots

- Login and signup pages.
- User dashboard with quiz and learning buttons.
- Interactive quiz screen with question navigation.
- Grammar, Vocabulary, Speaking, Listening, and Exercise course pages.
- Final result page showing detailed performance.
- Admin dashboard to manage users and import questions.

--- 

## Features

### User Features
- Users stored in `backend/eplanet_users.db`.
- User registration and login with **ID** and **password**.
- Multiple levels **(Elementary, Pre-intermediate, Intermediate, Upper-intermediate, Advanced)**.
- Access to course pages:
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
- Admin login via session.
- View registered users with **performance stats**.
- Add questions manually or import from **JSON/Excel**.
- Upload question assets **(images/audio)**.

---

### Quiz Logic
- Questions stored in `backend/quiz_questions.db`.
- Assets stored in `assets/images/` and `assets/audio/`.
- Correct/wrong answers saved per user in `eplanet_users.db`.

---

### Lessons Logic
- Lessons stored in `backend/lessons/grammar.db`,  `backend/lessons/vocabulary.db`.. etc
- Assets stored in `assets/images/` and `assets/audio/`.
- Correct/wrong answers for the exercises displayed in real-time.

---

## Technologies Used

- **Python** : Core programming language.
- **Flet** : UI framework for building apps with Flutter-like widgets in Python.
-  **SQLite3** : Lightweight embedded database. 
- **JSON / Excel** : Question import support.

---

## Instalation 

1. Clone the repo : 

```bash
   git clone https://github.com/Rayen-CHAOUI/eplanet-quiz.git
```
```bash
    cd eplanet-quiz
```

2. install dependencies : 

```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install flet[all] 
```

3. Run the app : 

```bash
    python3 main.py
```

---

##  Upcoming Improvements

- Timer per question.
- Question categories (Grammar, Listening, etc.). ---> **DONE**
- User statistics and progress tracking.
- Export results to PDF.

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