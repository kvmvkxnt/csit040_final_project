# Mall Gaming Booth Analysis

## Project overview

This project aims to identify the **best mall**, **day**, and **time** to open a
gaming booth using a dataset of mall visitors. The dataset includes details
about visitors' **age group**, **day of the week**, **time of visit**, and
**total bill spent**.

By analyzing these factors, we determine:

1. Which mall has the highest potential for a gaming booth.
2. The best time of day to attract the target audience.
3. The day of the week with the highest engagement and spending.

The goal is to provide data-driven recommendations for maximizing booth profitability
and engagement.

## Dataset Description

| Column          | Description                                   |
| --------------- | --------------------------------------------- |
| Mall            | Name of the mall (3 options)                  |
| Age Group       | Visitor age group (e.g 10-20, 21-30, etc.)    |
| Day of the week | Day the visitor came (Monday-Sunday)          |
| Time of the day | Period of visit (Morning, Afternoon, Evening) |
| Total Bill      | Total amount spent during the visit           |

## Installation & Setup

Follow these steps to run the project locally.

1. Clone the repository

```bash
git clone https://github.com/kvmvkxnt/csit040_final_project
cd csit040_final_project
```

2. Create a virtual environment

```bash
python -m venv .venv
```

3. Activate the virtual environment

- Windows:

```powershell
.venv\Scripts\activate
```

- macOs/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

From now on, you can launch the program with `python main.py` or build an executable.
Or even download pre-built. To build an executable for your system, follow next steps.

5. Build an executable

- macOs/Linux/Windows:

```bash
pyinstaller --onedir --windowed --noconfirm --clean --noupx main.py
```

Executable will be located in `dist/` directory and you can launch it from here.
Otherwise, download pre-built executable from [Releases](link).

6. Using Github Releases.

- macOs:
  Download macOs release for your system, unzip and just drag the .app to your Applications
  folder.
- Windows:
