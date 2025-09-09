# Project Scoping Questions for ML Software Development

## 1. Problem Definition

### What real-world problem are you addressing, and why is it important?

The project aims to predict the outcome of a chess match after the opening phase. The model will return a probability distribution over the three possible outcomes: White wins, Black wins, or a draw.

Understanding the likely outcome early in the game can provide valuable insights for players seeking to improve their decision-making and game strategy. Unlike traditional chess engines that provide evaluations in centipawns, this approach focuses on outcome probabilities, which are more interpretable and aligned with the final result of the game.

### Who are the target users or stakeholders of your system?

1. Amateur and intermediate chess players who want to analyze their games and identify weaknesses in the transition from opening to mid-game.

1. Coaches and trainers, who can use the model as a complementary tool for evaluating students’ games and highlighting opening choices that correlate with favorable outcomes.

1. Chess enthusiasts and researchers, who may be interested in the statistical properties of chess outcomes based on game states.

### Is the problem supervised, unsupervised, reinforcement, or a hybrid ML task? Choose one and explain

The problem is supervised learning. The dataset consists of completed games from the Lichess database, where each game includes the sequence of moves, metadata (e.g., time control, ratings), and the final result. The labels (outcome: White win, Black win, or draw) are already available, making this a classification task.

## 2. Data Considerations

### What kind of data will you use (structured, unstructured, multimodal)?

The data is structured. It contains categorical, numerical, and sequential elements:

Categorical: opening played, player ratings, time control.

Sequential: move sequences.

Numerical: number of moves, time remaining.

### Do you already have access to the data? (Yes/No) - If not, look for a dataset you have access to.

Yes. The Lichess database provides free, open access to historical game records.

### Can the data be used openly in academic projects? (Yes/No) - If not, look for a different dataset.

Yes, the dataset is openly available and can be used for academic purposes.

### What is the expected size and quality of the dataset? Does the data require cleaning?

The dataset is large, all the games from the month of July 2025 are over 200GB in size. I will have to decide on the scope of my project when looking with more detail the data what timeframe I want to model and what level of players.

Preprocessing will be necessary to:

Extract the game state representation after the opening.

Encode moves and board positions in a machine-readable format.

Filter out corrupted or incomplete games.

This cleaning ensures the ML algorithm can learn effectively from the data.

## 3. System Design & Software Architecture

### Which technology would you like to use for the different components of the ML Pipeline?

#### Frontend

- [x] Streamlit (recommended)
- [ ] Gradio
- [ ] FastHTML
- [ ] Other

#### REST API

- [x] FastAPI (recommended)
- [ ] Flask
- [ ] Django-Rest
- [ ] Other

#### Experiment Tracking

- [ ] MLFlow
- [x] Weights and Biases (recommended)
- [ ] Neptune

#### Hyperparameter Tuning

- [x] Optuna (recommended)
- [ ] HyperOpt
- [ ] Tune

#### Dataprocessing Library

- [ ] Pandas
- [x] Polars
- [ ] PySpark
- [ ] Narwhals

#### Machine Learning Framework

- [x] Scikit Learn (recommended)
- [x] FastAI
- [ ] Keras
- [ ] Pytorch Lightning
- [ ] PyMC

#### SQL Database

- [ ] Supabase (recommended)
- [ ] Vercel (Postgres)
- [ ] Other

#### NoSQL Database (Optional)

- [ ] Firebase (recommended)
- [ ] Other

#### Storage

- [ ] Supabase Blobs (recommended)
- [ ] Other

#### Testing Framework

- [x] Pytest (recommended)
- [ ] Unittest


## 4. Model Development & Lifecycle

### Do you plan to build models from scratch or leverage pre-trained models?

The initial models will be developed from scratch. The plan is to first exclude chess engine evaluations to avoid over-dependence on expert systems. If model performance is insufficient, engine evaluations may later be incorporated as additional features.

### What criteria will you use to define model success beyond accuracy (e.g., fairness, latency, robustness)?

Since games can get wild and unpredictable, especially after the opening, and blunders can occur at any stage of the game I will look for robustness as an additional criteria for model evaluation

## 5. Testing & Quality Assurance

### How will you test your system end-to-end, especially around ML-specific challenges (e.g., non-determinism, drift)?

* Unit and integration tests using Pytest for data pipelines, feature engineering, and API endpoints.

* Cross-validation to ensure robustness of the model across different subsets of the data.

* Out-of-distribution testing by evaluating on games with games that are unseen by the model

## 6. Deployment & Operations

### Will your system run in batch mode, real-time, or hybrid?

Real-time mode via FastAPI endpoints for evaluating a single position during or after a live game.

### How will you monitor the system for performance degradation and data drift?

* Model performance monitoring: periodic re-evaluation against newly played games to ensure predictions remain calibrated.

* Data drift monitoring: comparing statistical properties of new input data to the training dataset.
