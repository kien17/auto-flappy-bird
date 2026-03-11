# 🐦 Flappy Bird AI - Neuroevolution Simulation

A simulation project where **1000 AI birds learn to play Flappy Bird automatically** using **Genetic Algorithms** and **Neural Networks**.
Over generations, the population evolves better strategies to avoid obstacles and survive longer.

---

## 🚀 Features

* **Large Population Simulation**
  Simulate **1000 birds simultaneously** in each generation.

* **Neuroevolution Learning**
  Birds evolve through **selection, crossover, and mutation**.

* **Fitness Evaluation**
  Score is calculated based on:

  * Distance traveled
  * Pipes successfully passed

* **Real-time Learning Visualization**
  Watch the birds become smarter generation after generation.

---

## 🧠 How It Works

This project uses a **Neuroevolution approach**, combining **Genetic Algorithms** with **Neural Networks**.

### 1. Initialization

Create **1000 birds with random neural network weights**.

### 2. Decision Making

Each bird decides **whether to jump or not** based on:

* Distance to the next pipe
* Bird's current velocity
* Bird's vertical position

### 3. Selection

When all birds die, the algorithm selects the **best-performing individuals (elite birds)**.

### 4. Crossover & Mutation

New birds are created by:

* Combining parent neural network weights
* Applying **random mutations** to explore new strategies

This evolutionary cycle repeats for many generations.

---

## 🛠 Technologies Used

* **Language:** Python
* **Libraries:**

  * Pygame
  * NumPy
* **Algorithms:**

  * Genetic Algorithm
  * Feedforward Neural Network

---

## 📦 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/kien17/auto-flappy-bird.git
cd auto-flappy-bird
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the simulation

```bash
python main.py
```

---

## 📈 Results

After around **50+ generations**, the algorithm typically discovers a **highly optimized bird** capable of surviving extremely long and passing many obstacles without crashing.

You can visually observe:

* Evolution of strategies
* Increasing average fitness
* Emergence of elite birds

---

## 📂 Project Structure

```
auto-flappy-bird/
│
├── __pycache__/
│
├── background.png
├── Mimi_fly.png
├── Mimi_roi.png
│
├── bird.py
├── game.py
├── game_for_bot.py
├── genetic_bot.py
├── neuron_for_genetic.py
├── main.py
│
└── README.md
```

---

## 🤝 Contributing

Contributions, improvements, and new ideas are welcome!

If you'd like to improve the algorithm or optimize performance:

1. Fork the repository
2. Create a new branch
3. Submit a pull request

---

## 📬 Contact

If you're interested in AI, simulations, or game AI, feel free to connect:

GitHub: https://github.com/kien17

---

⭐ If you like this project, consider giving it a **star** on GitHub!
