# MindPulse AI 🧠

> **A multimodal deep-learning system for early detection of changing student stress and emotional-wellness patterns.**

MindPulse AI is a research-oriented AI system designed to analyze multiple signals — **journal text, voice, behavioral/contextual data, and optional facial/video information** — and model how these signals change over time.

The goal is not to diagnose mental-health disorders. Instead, MindPulse AI acts as an **early-warning and wellness-support system**, helping identify potentially concerning changes and providing supportive, personalized recommendations.

---

## 📌 Table of Contents

- [Problem](#-problem)
- [Solution](#-solution)
- [Key Idea](#-key-idea)
- [System Architecture](#-system-architecture)
- [Deep Learning Models](#-deep-learning-models)
- [Data Flow](#-data-flow)
- [Core Features](#-core-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Training Strategy](#-training-strategy)
- [Evaluation](#-evaluation)
- [Hackathon MVP](#-hackathon-mvp)
- [Future Extensions](#-future-extensions)
- [Safety & Privacy](#-safety--privacy)
- [Team Goal](#-team-goal)

---

## 🚨 Problem

Students can experience gradually increasing:

- Academic pressure
- Stress
- Emotional exhaustion
- Sleep disruption
- Social isolation
- Financial pressure
- Relationship difficulties
- Loss of motivation
- Burnout-related symptoms

These changes may develop over several days or weeks.

Many existing wellness applications rely primarily on:

- Questionnaires
- Single-session assessments
- Basic sentiment analysis
- Simple rule-based systems

A major limitation is that emotional states are **dynamic and multimodal**.

A single journal entry cannot necessarily represent a student's overall state.

For example:

```text
Day 1 → Normal
Day 2 → Slightly stressed
Day 3 → More workload
Day 4 → Poor sleep
Day 5 → Negative journal language
Day 6 → Increased stress indicators
Day 7 → Significant change from baseline
```

MindPulse AI focuses on detecting this **trajectory**, rather than relying only on a single prediction.

---

# 💡 Solution

MindPulse AI combines multiple deep-learning models into a single multimodal and longitudinal architecture.

### Input

```text
Journal + Voice + Behavior + Optional Video
```

### Processing

```text
Individual Deep Learning Encoders
              ↓
       Multimodal Fusion
              ↓
      Temporal Transformer
              ↓
       Multi-Task Learning
              ↓
      Explainability Layer
              ↓
      Support Recommendation
```

### Output

The system provides:

- Current AI-generated wellness indicators
- Recent trend/trajectory
- Contributing signals
- Changes compared with recent history
- Personalized supportive recommendations

---

# 🎯 Key Idea

The main research idea is:

> **Don't only ask "How is the student today?" — model "How is the student's state changing over time?"**

Every interaction generates a multimodal representation.

```text
Day 1 ──► Multimodal Embedding
Day 2 ──► Multimodal Embedding
Day 3 ──► Multimodal Embedding
Day 4 ──► Multimodal Embedding
...
Day N ──► Multimodal Embedding
                │
                ▼
       Temporal Transformer
                │
                ▼
       Longitudinal Pattern
```

This allows the system to model trends instead of treating every day as an independent prediction.

---

# 🏗 System Architecture

```text
                         ┌──────────────────────┐
                         │      STUDENT APP     │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
        ┌───────────┐         ┌───────────┐         ┌───────────┐
        │   TEXT    │         │   VOICE   │         │  VIDEO    │
        │  JOURNAL  │         │  RECORDING│         │  OPTIONAL │
        └─────┬─────┘         └─────┬─────┘         └─────┬─────┘
              │                     │                     │
              ▼                     ▼                     ▼
        ┌───────────┐         ┌───────────┐         ┌───────────┐
        │ BERT /    │         │ wav2vec2  │         │ ViT / CNN │
        │ RoBERTa   │         │ / HuBERT  │         │           │
        └─────┬─────┘         └─────┬─────┘         └─────┬─────┘
              │                     │                     │
              ▼                     ▼                     ▼
        Text Embedding        Voice Embedding       Visual Embedding
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │    BEHAVIORAL FEATURES      │
                     │ Sleep / Workload / Activity │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │      MULTIMODAL FUSION       │
                     │                             │
                     │  Cross-Attention Transformer│
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │    TEMPORAL TRANSFORMER      │
                     │                             │
                     │   Day 1 → Day N             │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │     MULTI-TASK HEADS         │
                     ├─────────────────────────────┤
                     │ Stress Indicator             │
                     │ Emotional Exhaustion         │
                     │ Risk Trajectory              │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     ▼                             ▼
          ┌─────────────────────┐       ┌─────────────────────┐
          │  EXPLAINABILITY     │       │ SUPPORT ENGINE      │
          │                     │       │                     │
          │ SHAP / Grad-CAM     │       │ Personalized        │
          │ Attention           │       │ Recommendations     │
          └──────────┬──────────┘       └──────────┬──────────┘
                     │                             │
                     └──────────────┬──────────────┘
                                    ▼
                     ┌─────────────────────────────┐
                     │       USER DASHBOARD         │
                     │                             │
                     │ Current indicators           │
                     │ 7/14-day trends              │
                     │ Contributing signals         │
                     │ Personalized support         │
                     └─────────────────────────────┘
```

---

# 🤖 Deep Learning Models

## 1. Text Encoder

### Candidate Models

- BERT
- RoBERTa
- DeBERTa

### Pipeline

```text
Journal Entry
     ↓
Tokenizer
     ↓
Transformer Encoder
     ↓
Contextual Embedding
     ↓
Text Representation
```

The text encoder extracts semantic and contextual information from journal entries.

---

## 2. Speech Encoder

### Candidate Models

- wav2vec 2.0
- HuBERT

### Pipeline

```text
Voice Recording
     ↓
Audio Preprocessing
     ↓
Speech Encoder
     ↓
Frame-level Representations
     ↓
Temporal Pooling
     ↓
Voice Embedding
```

The speech model provides an acoustic representation that becomes one input to the multimodal system.

---

## 3. Visual Encoder

### Candidate Models

- Vision Transformer (ViT)
- CNN-based visual encoder

### Pipeline

```text
Video
 ↓
Face Detection
 ↓
Frame Extraction
 ↓
ViT / CNN
 ↓
Frame Embeddings
 ↓
Temporal Aggregation
 ↓
Visual Representation
```

The visual component is optional and should require explicit user consent.

---

## 4. Behavioral Encoder

Behavioral/contextual data can include:

- Sleep duration
- Study hours
- Workload
- Physical activity
- Daily stress rating
- Mood check-in
- Number of tasks

Pipeline:

```text
Behavioral Data
      ↓
Normalization
      ↓
MLP / Small Transformer
      ↓
Behavior Embedding
```

---

# 🔀 Multimodal Fusion

Each modality produces an embedding:

```text
Text Embedding
      │
Voice Embedding
      │
Visual Embedding
      │
Behavior Embedding
      │
      ▼
Multimodal Transformer
      │
      ▼
Cross-Attention
      │
      ▼
Unified Representation
```

The system can experiment with cross-attention rather than simply concatenating features.

This is one of the project's primary deep-learning research components.

---

# ⏳ Temporal Modeling

The system maintains a sequence of daily multimodal representations.

```text
Day 1 → Embedding
Day 2 → Embedding
Day 3 → Embedding
...
Day 14 → Embedding
       ↓
Temporal Transformer
       ↓
Longitudinal Representation
       ↓
Trend Prediction
```

### Candidate Models

- LSTM
- GRU
- Temporal Transformer

The primary proposed architecture is a **Temporal Transformer**.

---

# 🎯 Multi-Task Learning

A shared representation feeds multiple prediction heads:

```text
                 Shared Representation
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Stress       Emotional       Risk
       Indicator    Exhaustion      Trajectory
```

This allows the model to learn several related tasks using a shared multimodal representation.

---

# 🔍 Explainable AI

MindPulse AI should not simply output a number.

Example:

```text
Recent Wellness Trend

Stress-related signals     ████████████████
Sleep pattern              █████████████
Workload                    ███████████
Voice signals               ████████
Visual signals              █████
```

Potential explainability techniques:

- SHAP
- Grad-CAM
- Attention visualization
- Text attribution

These explanations represent **model-attribution signals**, not clinical explanations.

---

# 💬 Personalized Support Engine

The prediction system provides structured outputs to a support engine.

```text
Model Output
     ↓
Trend Information
     ↓
Context
     ↓
Recommendation Engine
     ↓
Personalized Support
```

Possible support actions:

- Suggest a short break
- Recommend workload planning
- Encourage a healthier sleep routine
- Suggest relaxation activities
- Encourage connecting with a trusted person
- Encourage professional support when appropriate

The language model should operate on structured model outputs and should not independently diagnose a user.

---

# 🔄 Complete Data Flow

```text
User Interaction
      ↓
┌─────────────────────────────────────┐
│ Text │ Voice │ Behavior │ Video    │
└─────────────────┬───────────────────┘
                  ↓
          Modality Encoders
                  ↓
       Multimodal Embeddings
                  ↓
      Cross-Attention Fusion
                  ↓
       Temporal Transformer
                  ↓
        Multi-Task Prediction
                  ↓
      ┌───────────┴───────────┐
      ↓                       ↓
Explainability          Support Engine
      │                       │
      └───────────┬───────────┘
                  ↓
             Dashboard
```

---

# ✨ Core Features

### 📝 Smart Journal

Students can write daily journal entries that are analyzed using a Transformer model.

### 🎙️ Voice Check-In

Students can optionally record a short voice note.

### 📊 Longitudinal Dashboard

Visualizes changes over:

- 7 days
- 14 days
- 30 days

### 🧠 Multimodal AI

Combines multiple sources instead of relying on a single modality.

### 📈 Trend Detection

Focuses on changes over time.

### 🔍 Explainability

Shows which signals contributed to the model's output.

### 💬 Personalized Support

Provides context-aware wellness suggestions.

### 🔐 Privacy-Aware Design

Sensitive information should be collected only with appropriate consent and handled securely.

---

# 🛠️ Technology Stack

## Deep Learning

- Python
- PyTorch
- Hugging Face Transformers
- BERT / RoBERTa / DeBERTa
- wav2vec 2.0 / HuBERT
- Vision Transformer
- Temporal Transformer

## Machine Learning

- NumPy
- Pandas
- Scikit-learn

## Explainability

- SHAP
- Grad-CAM
- Attention Visualization

## Backend

- FastAPI
- PostgreSQL / Supabase

## Frontend

- React
- TypeScript
- Material UI

## Deployment

- Docker
- GPU inference where available

---

# 📁 Proposed Project Structure

```text
mindpulse-ai/
│
├── README.md
├── requirements.txt
├── docker-compose.yml
│
├── backend/
│   ├── api/
│   ├── services/
│   ├── schemas/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│
├── models/
│   ├── text/
│   ├── speech/
│   ├── vision/
│   ├── behavioral/
│   ├── fusion/
│   └── temporal/
│
├── training/
│   ├── datasets/
│   ├── preprocessing/
│   ├── train_text.py
│   ├── train_speech.py
│   ├── train_vision.py
│   ├── train_fusion.py
│   └── train_temporal.py
│
├── explainability/
│   ├── shap/
│   ├── gradcam/
│   └── attention/
│
├── notebooks/
│   ├── exploration/
│   └── experiments/
│
└── configs/
    ├── model.yaml
    └── training.yaml
```

---

# 🧪 Training Strategy

The project can be developed in stages.

## Stage 1 — Individual Modality Models

```text
Text → Text Encoder
Voice → Speech Encoder
Video → Vision Encoder
Behavior → MLP
```

Each encoder is evaluated independently.

## Stage 2 — Multimodal Fusion

```text
Text + Voice + Behavior
          ↓
Multimodal Transformer
```

Compare multimodal performance against individual modalities.

## Stage 3 — Temporal Modeling

```text
Daily Multimodal Representations
          ↓
Temporal Transformer
          ↓
Trend Prediction
```

## Stage 4 — Multi-Task Learning

Train multiple prediction heads using a shared representation.

## Stage 5 — Explainability

Integrate attribution and visualization methods into the inference pipeline.

---

# 📊 Evaluation

The system should be evaluated using quantitative metrics.

## Classification

- Accuracy
- Precision
- Recall
- F1-score
- AUROC
- AUPRC

## Regression

- MAE
- RMSE
- R²

## Temporal Evaluation

- Early-warning detection performance
- Trajectory prediction error
- Detection lead time

---

# 🔬 Ablation Study

One important experiment is to determine how much each modality contributes.

```text
Experiment 1
Text only

Experiment 2
Text + Voice

Experiment 3
Text + Voice + Behavior

Experiment 4
Text + Voice + Behavior + Video

Experiment 5
Full Model + Temporal Transformer
```

This allows the team to demonstrate whether multimodal and temporal learning provide measurable improvements.

---

# 🚀 Hackathon MVP

The complete architecture is ambitious, so the initial hackathon version should prioritize the core pipeline.

## MVP Architecture

```text
Journal
   ↓
Transformer
   ↓
Text Embedding
        +
Voice
   ↓
wav2vec2
   ↓
Voice Embedding
        +
Behavior
        ↓
Multimodal Fusion
        ↓
Temporal Transformer
        ↓
Risk Trajectory
        ↓
Dashboard
```

### Optional Advanced Components

If the core system is stable:

- Facial/video encoder
- Cross-attention visualization
- Multi-task learning
- SHAP explanations
- Grad-CAM
- Personalized LLM support
- Real-time inference

---

# 🎬 Example Demo

A student opens MindPulse AI.

### Step 1

The application asks:

> How was your day?

The student writes a short journal entry.

### Step 2

The student records a 30-second voice note.

### Step 3

The application collects optional contextual information:

```text
Sleep: 5.5 hours
Study: 8 hours
Workload: High
Self-reported stress: 7/10
```

### Step 4

The AI processes the information:

```text
Text Encoder
      +
Speech Encoder
      +
Behavior Encoder
      ↓
Multimodal Fusion
      ↓
Temporal Model
```

### Step 5

The dashboard shows the recent trajectory:

```text
7-Day Trend

Day 1   ███████
Day 2   ████████
Day 3   █████████
Day 4   ██████████
Day 5   ███████████
Day 6   █████████████
Day 7   ██████████████
```

### Step 6

The system presents a supportive message based on the model's detected trend.

---

# 🔐 Safety & Privacy

MindPulse AI is designed as a **wellness-support and early-warning system**, not as a replacement for:

- Psychologists
- Psychiatrists
- Therapists
- Doctors
- Emergency services

The system should:

- Obtain explicit consent for sensitive inputs
- Make video analysis optional
- Minimize personal-data collection
- Encrypt sensitive information
- Allow users to delete their data
- Avoid presenting model outputs as medical diagnoses
- Communicate uncertainty
- Provide appropriate guidance toward trusted humans or professional support when needed

The system should have an appropriate crisis/safety flow for users who indicate immediate danger or self-harm concerns.

---

# 🌟 Project Innovation

The project combines several modern deep-learning concepts:

```text
Transformer Language Model
          +
Self-Supervised Speech Model
          +
Vision Transformer
          +
Behavior Encoder
          +
Multimodal Cross-Attention
          +
Temporal Transformer
          +
Multi-Task Learning
          +
Explainable AI
```

The central research idea is:

> **Learn a longitudinal multimodal representation of a student's changing wellness-related patterns instead of making isolated single-session predictions.**

---

# 🎯 Research Question

> **Can longitudinal multimodal deep learning identify meaningful changes in a student's emotional and behavioral state earlier than single-modality or single-session approaches?**

---

# 📌 One-Line Project Description

> **MindPulse AI is a multimodal longitudinal deep-learning system that analyzes language, speech, behavior, and optional visual signals over time to identify changing wellness-related patterns and provide personalized supportive interventions.**

---

## ⚠️ Disclaimer

MindPulse AI is an experimental research/hackathon project intended for educational and wellness-support purposes. Its outputs are not medical diagnoses and should not be used as a substitute for professional medical or mental-health assessment.
