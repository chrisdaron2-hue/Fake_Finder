# 🕵️ Fake Finder: Fact or Fiction?
<img width="1024" height="1024" alt="Fake Finder" src="https://github.com/user-attachments/assets/c6b0050b-474a-4279-8a5f-51efd0e43d24" />

<img width="1232" height="546" alt="Screenshot 2025-11-02 at 00 17 00" src="https://github.com/user-attachments/assets/f0e91008-48e4-42b4-ad3f-bdcd094f55de" />

Fake Finder is an interactive command-line fact-checking game powered by Wikipedia and Google Gemini AI.
Your mission: identify the fake fact hidden among real ones!

---

## 🎯 Game Overview

Fake Finder challenges players to distinguish true statements from AI-generated fake ones, based on Wikipedia articles.
Each round presents four sentences — one is false, and three are true.
Your goal is to pick the fake one and test your knowledge across categories like Science, Lifestyle, and Politics.

---

## 🧩 Features

- 🎮 Interactive command-line gameplay
- 🧠 Real facts sourced from Wikipedia
- 🤖 AI-powered fake fact generation using Google Gemini
- 🧭 Multiple categories and topics
- ⚙️ Difficulty levels: Easy, Medium, Hard
- 🧾 Score tracking and replay options
- ✨ Animated “searching for facts” visual effect

---
## 🎮 Example Gameplay
<img width="890" height="1044" alt="Screenshot 2025-11-02 at 00 25 11" src="https://github.com/user-attachments/assets/29fb272a-3212-40ea-b029-07a5bda858c3" />
<img width="890" height="1008" alt="Screenshot 2025-11-02 at 00 27 35" src="https://github.com/user-attachments/assets/05dc9740-1f06-494d-8325-0901d4b28879" />

---

## 🧠 How It Works

1. Choose your ***name***, ***difficulty***, and ***number of rounds***.
2. Select a ***category*** and a topic (e.g., Science → DNA)
3. The system fetches real data from Wikipedia
4. The ***Gemini AI*** model generates 3 true and 1 fake statements
5. You must guess which statement is fake
6. Earn points for each correct answer — try to get a perfect score!

---

## 🧰 Tech Stack
```Bash
| Component              | Technology                                                                  |
| ---------------------- | --------------------------------------------------------------------------- |
| Programming Language   | Python 3.9+                                                                 |
| AI Model               | Google Gemini 2.5 Flash                                                     |
| Knowledge Source       | Wikipedia API                                                               |
| Environment Management | python-dotenv                                                               |
| Animation              | Threading + ASCII                                                           |
| Libraries              | `wikipedia`, `google-genai`, `dotenv`, `threading`, `sys`, `time`, `random` |

```

---
## ⚙️ Installation
### 1. Clone the Repository
```Bash
git clone https://github.com/abhisakh/fake-finder.git
cd fake-finder

```
### 2. Create and Activate a Virtual Environment
```Bash
python -m venv venv
source venv/bin/activate   # on macOS/Linux
venv\Scripts\activate      # on Windows

```
### 3. Install Dependencies
```Bash
pip install -r requirements.txt

```

### 4. Set Up Environment Variables

Create a .env file in the project root with:
```Bash
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 5. Run the Game
```Bash
python fake_finder.py
```
---
## 📁 Project Structure
fake_finder/
│
├── main.py       # Main game logic
├── .env                 # Environment variables (not tracked by Git)
├── requirements.txt     # Dependencies
└── README.md            # Documentation

---
## 🧑‍💻 Requirements

- Python 3.9 or higher
- Internet connection (for Wikipedia + Gemini API access)
- Google Gemini API key (Get one here)

---

## 🧠 Future Improvements

- 🌐 Web-based interface using Flask + JavaScript
- 💾 Persistent player stats (database or JSON)
- 🎨 Improved animations and UI
- 🏆 Leaderboard system
- 📊 Game analytics & difficulty tuning

---

## 🙋‍♂️ Authors (Hackathon 2025, MasterSchool, Berlin)
1. **Abhisakh Sarma**
GitHub: [https://github.com/abhisakh](https://github.com/abhisakh)

2. **Johannes Mashegwana**

3. **Elizabeth Gyamfi**

4. **Henrik Horn**

5. **Anuj Nandy**

I upgraded the project by myself to a webbased online Game.....named Fake_Finder_Webintegration(Hope you will enjoy )


_Contributions and feedback are always welcome!_

🌐 GitHub Profile










