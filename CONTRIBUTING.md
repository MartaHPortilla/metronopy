# 🤝 Contributing to Metronopy

Thank you for your interest in contributing to Metronopy!
This project values clean architecture, clear responsibilities, and musical accuracy, so please take a moment to read these guidelines before contributing.

## 🧭 Project Philosophy

Metronopy is intended to be built around a few core principles:

- 🎯 Single Responsibility: each module does one thing, and does it well
- ⏱️ Metronome as the source of truth: timing always flows from Metronome
- 🧠 Explicit domain modeling: beats, timing, and types are first-class concepts
- 🧩 Loose coupling: builders and composer depend on abstractions, not implementations
- 🧪 Readability over cleverness

If a change violates these principles, it’s probably not a good fit.

## 🛠️ How to Contribute

### 1️⃣ Fork the repository

Create a fork and work on your own copy.

### 2️⃣ Create a feature branch

```bash
git checkout -b feature/short-description 

#example: feature/time_signatures
```

### 3️⃣ Follow the Coding Standards

- Python Style
- PEP 8
- Use type hints consistently
- Prefer explicit names over abbreviations
- Keep functions small and focused

✅ Good:

```python
def seconds_per_beat(self) -> float:
    ...
```

❌ Please avoid:

```python
    def spb(self):
    ...
```

## 🧩 Module Responsibilities

Please do not mix responsibilities across modules.

| Module         | Should                   | Should NOT          |
| -------------- | ------------------------ | ------------------- |
| `Metronome`    | Timing, beats, durations | Audio, video, files |
| `AudioBuilder` | Audio generation         | Timing logic        |
| `VideoBuilder` | Video generation         | Audio logic         |
| `Composer`     | Orchestration            | Business rules      |
| `__main__`     | Wiring & execution       | Logic               |

## 🧪 Testing

Currently, the project does not include automated tests, but they are on the way. I will be extremely satisfied if new features are manually tested, isolated, readable and do not break the existing behaviour.

## 📝 Documentation

If you add or change behaviour:

- Update docstrings
- Update README.md if relevant
- Keep comments why-focused, not what-focused

    ✅ Good comment:

    ```python
    # Timing must come from Metronome to avoid drift
    ```

    ❌ Not a good comment:

    ```python
    # This adds two numbers
    ```

## 🧹 Temporary Files & Resources

- Always close audio/video resources explicitly
- Never assume the OS will clean up for you
- Temporary files must be handled safely, especially on Windows

## 📦 Commit Messages

Please use clear, descriptive commit messages:

✅ Good:

```bash
Add support for custom time signatures
Fix temp audio file cleanup on Windows
Refactor VideoBuilder typing
```

❌ Not good:

```bash
stuff
fix
changes
```

## 💬 Questions & Discussions

If you’re unsure about:

- 🧠 Architecture decisions
- ✨ Where a feature should live
- 📦 Whether something fits the project

👉 Please feel free to open an issue or discussion.

## 🙌 Code of Conduct

Be respectful, constructive and patient. This project is built for learning as much as for functionality.

Thanks for contributing 💙
