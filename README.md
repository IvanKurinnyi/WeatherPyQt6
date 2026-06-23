
# 🌦️ Weather App (PyQt6)


This repository contains a bilingual desktop application for tracking weather conditions, built using Python and PyQt6.
Цей репозиторій містить двомовний десктопний застосунок для відстеження погодних умов, створений за допомогою Python та PyQt6.

--- 

Language selection / Вибiр мови:
[🇬🇧 English Version](#-english-version) | [🇺🇦 Українська версія](#-українська-версія)

---

# 🇬🇧 English Version

## 📋 Table of Contents
1. [Project Purpose](#1-project-purpose)
2. [Team Composition](#2-team-composition)
3. [List of Modules and Technologies](#3-list-of-modules-and-technologies)
4. [How to Run the Project](#4-how-to-run-the-project)
5. [Project Structure and Components](#5-project-structure-and-components)
6. [Conclusion and Future Development](#6-conclusion-and-future-development)
7. [License](#7-license)

---

## 1. Project Purpose
The **Weather App** was designed to provide a comprehensive, real-time weather tracking solution with an intuitive graphical user interface. 
For a beginner developer, this project serves as an excellent practical guide to:
* Understanding the fundamentals of event-driven programming and desktop GUI architecture using **PyQt6**.
* Learning how to securely interact with third-party REST APIs (**OpenWeatherAPI**) using environment variables (`.env`).
* Integrating dynamic web-based geospatial data into a native desktop application via **Folium** and QtWebEngine.
* Implementing multi-language localization and responsive design adjustments in a Python ecosystem.

---

## 2. Team Composition
* **Ivan Kurinnyi** – Lead Developer / UI Developer — [GitHub Profile](https://github.com/IvanKurinnyi)
* **Artem Ostapenko** – Core Logic & API Developer — [GitHub Profile](https://github.com/Prleksei)

---

## 3. List of Modules and Technologies
### Core Technologies:
* **Python**: Core programming language.
* **PyQt6**: Framework used for building the cross-platform desktop user interface.
* **OpenWeatherAPI**: External REST service providing real-time weather metrics and forecasting data.
* **Folium**: Library utilized for generating interactive maps containing geographic coordinates.

### Key Modules:
* `main.py`: Entry point of the application responsible for configuring the environment and initializing the GUI loop.
* `weather_service.py` (or integrated fetcher): Manages asynchronous network requests to OpenWeatherAPI and parses JSON responses.
* `map_handler.py`: Generates localized HTML map components via Folium to display city coordinates dynamically.

---

## 4. How to Run the Project

### Prerequisites
Ensure you have Python 3.10+ installed on your operating system.

### Step-by-Step Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/IvanKurinnyi/WeatherPyQt6.git](https://github.com/IvanKurinnyi/WeatherPyQt6.git)

```

2. **Navigate to the project folder:**

```bash
cd weather_app

```

3. **Install dependencies:**

```bash
pip install -r requirements.txt

```

4. **Configuration (.env):**
Obtain a free API key from [OpenWeatherAPI](https://openweathermap.org/) and create a `.env` file in the root directory:

```env
API_KEY=your_api_key_here

```

5. **Run the application:**

```bash
python main.py

```

---

## 5. Project Structure and Components

The application consists of multiple view-states, interfaces, and modular components described below along with visual references:

### Main Window
Provides a summary of current weather indicators (temperature, weather state, humidity, and wind velocity) coupled with an embedded interactive map.

![Main Window](media/screenshots/en_image1.png)

### City Search Module
Allows users to look up precise weather metrics for any specific town or global coordinates with automated exception handling for invalid inputs.

![City Search Module](media/screenshots/en_image2.png)

### App Size Adjuster
Features a highly responsive UI layout engine that scales gracefully to adapt to various window geometries and screen configurations.

![App Size Adjuster](media/screenshots/en_image3.png)

### Localization / Language Toggle
Supports rapid state shifting between English and Ukrainian localizations, transforming all static text and API response mapping dynamically.

![Localization / Language Toggle](media/screenshots/en_image4.png)

### Image and Visual Assets Management
Handles icon caching and system asset matching corresponding directly to current meteorological states.

![Image and Visual Assets Management](media/screenshots/en_image5.png)

---

## 6. Conclusion and Future Development

### Key Takeaways:

Through the development lifecycle of this application, our team mastered hands-on multi-threading workflows in Python GUI setups (preventing UI freezes during API requests), cross-component communication inside PyQt signal architectures, and rendering localized HTML views natively.

### Roadmap for Future Enhancements:

1. **Historical Data Trends**: Implement historical data parsing and integrate Matplotlib/PyQtGraph to display temperature curves over past weeks.
2. **Offline Data Caching**: Integrate an SQLite database layer to store localized data, allowing users to view the last searched cities without active internet access.
3. **Advanced Alerts**: Set up system tray notifications for dangerous local weather alerts.

---

## 7. License

This project is licensed under the MIT License - see the LICENSE file for details.

---

---

# 🇺🇦 Українська версія

## 📋 Зміст файлу

1. [Мета створення проєкту]
2. [Склад команди]
3. [Перелік модулів та технологій]
4. [Як запустити проєкт в роботу]
5. [Зміст проєкту та компоненти]
6. [Висновок по роботі та плани розвитку]
7. [Ліцензія]

---

## 1. Мета створення проєкту

**Weather App** — це повнофункціональний десктопний застосунок для моніторингу погоди в реальному часі зі зручним графічним інтерфейсом.
Для розробника-початківця цей проєкт є чудовою практичною базою, яка допомагає:

* Опанувати фундаментальні принципи подієво-орієнтованого програмування та архітектури десктопного UI за допомогою фреймворку **PyQt6**.
* Навчитися безпечно взаємодіяти із зовнішніми REST API-сервісами (**OpenWeatherAPI**) із використанням змінних оточення (`.env`).
* Освоїти інтеграцію інтерактивних веб-карт усередину нативного вікна програми за допомогою зв'язки **Folium** та компонентів QtWebEngine.
* Реалізувати механізм динамічної локалізації (багатомовності) та адаптивної верстки інтерфейсу.

---

## 2. Склад команди

* **Іван Курінний** – Головний розробник / Розробник інтерфейсу — [Профіль GitHub](https://github.com/IvanKurinnyi)
* **Артем Остапенко** – Розробник внутрішньої логіки та iнтеграцiї API — [Профіль GitHub](https://github.com/Prleksei)

---

## 3. Перелік модулів та технологій

### Основний технологічний стек:

* **Python**: Основна мова програмування проєкту.
* **PyQt6**: Кросплатформний фреймворк для побудови графічного інтерфейсу користувача.
* **OpenWeatherAPI**: Зовнішній REST сервіс для отримання актуальних метеорологічних даних та прогнозів.
* **Folium**: Бібліотека для генерації інтерактивних HTML-карт на основі геокоординат.

### Опис ключових модулів:

* `main.py`: Головна точка входу в застосунок, яка налаштовує конфігурацію середовища та запускає головний цикл обробки подій UI.
* `api_request.py` : Відповідає за виконання мережевих запитів до API, обробку можливих помилок зв'язку та парсинг JSON-відповідей.

---

## 4. Як запустити проєкт в роботу

### Системні вимоги

Переконайтеся, що на вашому комп'ютері встановлено Python версії 3.10 або вище.

### Покрокова інструкція із розгортання

1. **Клонуйте репозиторій із кодом проєкту:**

```bash
git clone [https://github.com/IvanKurinnyi/WeatherPyQt6.git](https://github.com/IvanKurinnyi/WeatherPyQt6.git)

```

2. **Перейдіть у кореневу директорію проєкту:**

```bash
cd weather_app

```

3. **Встановіть усі необхідні залежності:**

```bash
pip install -r requirements.txt

```

4. **Налаштування конфігурації (.env):**
Зареєструйтеся та отримайте безкоштовний API-ключ на сайті [OpenWeatherAPI](https://openweathermap.org/). Створіть файл `.env` у корені проєкту та додайте туди ваш ключ за прикладом:

```env
API_KEY=your_api_key_here

```

5. **Запустіть застосунок:**

```bash
python main.py

```

---

## 5. Зміст проєкту та компоненти

Застосунок складається з кількох взаємопов'язаних інтерфейсів та функціональних блоків:

### Головне вікно (Main Window)
Відображає поточні показники погоди (температура, вологість, швидкість вітру, загальний стан атмосфери) та містить інтегровану карту з маркером обраного міста.

![Головне вікно](media/screenshots/ua_image1.png)

### Пошук міста (City Search)
Модуль для введення назви населеного пункту з автоматичною валідацією запитів та коректним опрацюванням помилок у разі відсутності міста у базі даних.

![Пошук міста](media/screenshots/ua_image2.png)

### Розмір додатку (App Size Adjuster)
Реалізує логіку адаптивного лейауту (layout sizing), завдяки чому інтерфейс гнучко масштабується під різні екрани без втрати читабельності тексту.

![Розмір додатку](media/screenshots/ua_image3.png)

### Мова додатку (App Language / Localization)
Забезпечує миттєве перемикання між українською та англійською мовами інтерфейсу, перезаписуючи як статичні текстові мітки, так і локалізуючи відповіді від сервера погоди.

![Мова додатку](media/screenshots/ua_image4.png)

### Список зображень та асетів (Image Lists)
Керує динамічним завантаженням та відображенням іконок і графічних елементів, що відповідають поточному стану погоди (сонячно, дощ, гроза тощо).

![Список зображень та асетів](media/screenshots/ua_image5.png)

---

## 6. Висновок по роботі та плани розвитку

### Чому навчилися та чим корисний проєкт:

Під час розробки ми здобули практичний досвід роботи з асинхронністю в графічних інтерфейсах (використання потоків для запобігання зависанню вікна під час API-запитів), налаштували взаємодію між компонентами за допомогою механізму сигналів та слотів PyQt, а також навчилися працювати із вбудованим веб-рушієм для рендерингу карт.

### Напрямки подальшого розширення проєкту:

1. **Графіки та аналітика**: Додати модуль побудови графіків зміни температури протягом тижня (за допомогою бібліотек Matplotlib або PyQtGraph).
2. **Локальне кешування даних**: Впровадити базу даних SQLite для збереження історії пошуків та можливості перегляду останніх даних у режимі офлайн.
3. **Сповіщення про негоду**: Реалізувати фонову перевірку та надсилання системних tray-повідомлень у разі штормових попереджень.

---

## 7. Ліцензія

Цей проєкт поширюється під ліцензією MIT. Деталі дивіться у файлі LICENSE.

```

```