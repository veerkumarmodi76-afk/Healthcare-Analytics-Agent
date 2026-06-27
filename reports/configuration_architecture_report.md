# AI-AIP Configuration Architecture Report

## Overview

The `src/config` package is the central configuration layer of the AI-AIP project. It eliminates duplicated configuration across modules by providing one location for project paths, logging, constants, model parameters, and application settings.

Rather than allowing every pipeline to define its own paths and configuration, all modules should import the required objects from this package.

This architecture improves maintainability, readability, portability, and scalability.

---

# Configuration Package Structure

```
src/config
│
├── __init__.py
├── constants.py
├── logging_config.py
├── model_config.py
├── paths.py
└── settings.py
```

Each file has a single responsibility.

---

# 1. **init**.py

## Purpose

Acts as the public entry point for the configuration package.

Instead of importing multiple configuration files individually, modules can import directly from `src.config`.

Example:

```python
from src.config import Paths, Settings
```

This keeps imports concise and consistent.

---

# 2. paths.py

## Purpose

Provides a centralized definition of every filesystem path used throughout the project.

### Managed Directories

* Project Root
* Source Code
* Configuration
* Dashboard
* AI Copilot
* Raw Data
* Processed Data
* Model Storage
* Output Directories
* Reports
* Documentation
* Notebooks
* Temporary Files
* Logs

### Managed Files

* raw_data.csv
* processed_data.csv

### Pipeline Output Directories

* Preprocessing
* Underwriting
* Pricing
* Lapse
* Portfolio

### Benefits

* No hardcoded filesystem paths
* Platform-independent path handling
* Automatic directory creation
* Easier project relocation
* Consistent folder organization

Every module should obtain filesystem locations from `Paths`.

---

# 3. constants.py

## Purpose

Stores fixed values that rarely change.

Current examples include:

* Supported file extensions
* Model filenames
* Report filenames
* Risk class labels
* Underwriting decisions
* Logging format
* Plot defaults

### Benefits

* Removes repeated literal values
* Simplifies maintenance
* Ensures consistency across pipelines

---

# 4. logging_config.py

## Purpose

Provides centralized logging for the project.

### Features

* Console logging
* Rotating log files
* Consistent formatting
* Automatic log directory creation
* Duplicate handler prevention

### Recommended Usage

```python
from src.config.logging_config import get_logger

logger = get_logger(__name__)
```

Avoid using `logging.basicConfig()` inside production modules.

### Benefits

* Consistent logs
* Easier debugging
* Reduced duplicated code
* Automatic log rotation

---

# 5. model_config.py

## Purpose

Stores machine learning hyperparameters.

Current configurations include:

* Underwriting model
* Pricing model
* Lapse model

Training scripts should import these settings rather than embedding hyperparameters directly.

### Benefits

* Easier experimentation
* Better reproducibility
* Cleaner training code

---

# 6. settings.py

## Purpose

Stores global application settings.

Current settings include:

* Project version
* Random seed
* Train/test split
* Cross-validation folds
* Encoding
* Figure DPI
* Logging enablement
* SHAP enablement
* Explainability options

These values define how the application behaves globally.

---

# Configuration Flow

```
                   AI-AIP Project
                          │
                          ▼
                  src/config Package
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
      Paths          Settings         Constants
        │                 │                 │
        └─────────────┬───┴─────────────────┘
                      │
                 Logging & Models
                      │
                      ▼
        All Project Pipelines and Services
```

Every module should rely on this shared configuration layer instead of maintaining its own configuration.

---

# Responsibilities of Each Module

| File                | Responsibility                          |
| ------------------- | --------------------------------------- |
| `__init__.py`       | Public configuration interface          |
| `paths.py`          | Filesystem paths and directory creation |
| `constants.py`      | Shared constant values                  |
| `logging_config.py` | Standardized logging                    |
| `model_config.py`   | Machine learning hyperparameters        |
| `settings.py`       | Global application behavior             |

---

# Best Practices

Every production module should:

* Import filesystem paths from `Paths`.
* Import shared constants from `constants.py`.
* Use `get_logger()` for logging.
* Import model hyperparameters from `model_config.py`.
* Read global options from `settings.py`.

Production modules should not redefine paths, logging configuration, or shared constants.

---

# Supported Pipelines

The configuration package is designed to support all current project components:

* Data Preprocessing
* Underwriting
* Pricing
* Lapse Prediction
* Portfolio Analytics
* Dashboard
* AI Copilot
* Service Layer
* Validation Utilities

Future modules can be integrated without modifying the overall architecture.

---

# Future Expansion

The current design can easily accommodate:

* Environment variables
* Development, testing, and production profiles
* Cloud storage integration
* Database configuration
* API credentials
* Deployment configuration
* Docker support
* CI/CD pipelines

These additions can be implemented without changing the existing architecture.

---

# Conclusion

The AI-AIP configuration package serves as the foundation of the project's architecture. By centralizing paths, logging, constants, settings, and model parameters, it ensures consistency across every pipeline while minimizing duplicated code.

With the corrected `paths.py` and the existing supporting modules, the configuration layer is production-ready and provides a stable base for all subsequent development phases.
