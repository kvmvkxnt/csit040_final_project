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

## Presequities

Ensure you have git installed. On UNIX-based systems like MacOS, Linux, just
open your terminal app, and then run `git` command. If you see a long output,
then you have git installed. If you're on windows, open "PowerShell" terminal
(you can use search), and then do the same. You can install git from its
[official website](https://git-scm.com/install/windows).

And of course, ensure you have `python` installed.

On MacOS:

- Open `Terminal` application.
- Try running `python3 --version`.
  - If you see version below "3.13", you need to install python3 using `brew`.
    To install brew, follow the instruction on [Homebrew](https://brew.sh/)
    website. After you have installed brew, run `brew install python3@13`.
    This will install the required version of python to your system.

On Windows:

- Open `PowerShell` application. Use search tool to find it.
- Try running `python --version`.
  - If python is not installed, you will be redirected to Microsoft store to
    install it. Just install it, and you're good to go.

On Linux:

- If you use Linux, i don't have to explain you what to do.

## Installation & Setup

Follow these steps to run the project locally. On MacOs, use the `Terminal` app,
on Windows, use `PowerShell` app. Make sure to launch the `PowerShell` with
admin rights. Just copy and paste each command.

Clone the repository

```bash
git clone https://github.com/kvmvkxnt/csit040_final_project
cd csit040_final_project
```

Create and activate virtual environment

- Windows:

```bash
python -m venv .venv
Set-ExecutionPolicy ByPass  # After this command, type A
.venv\Scripts\activate
```

- macOs/Linux:

If you are using Mac with M-series chip, you need to use `/opt/homebrew/bin/python3.13`.
If you are using Mac with Inter chip, you need to use `/usr/local/bin/python3.13`

```bash
/opt/homebrew/bin/python3.13 -m venv .venv
source .venv/bin/activate
```

After the activation, you should see `(.venv)` before your command prompt.

Install dependencies

```bash
pip install -r requirements.txt
```

From now on, you can launch the program with `python main.py` or build an executable.
Or even download pre-built. To build an executable for your system, follow next steps.

**IMPORTANT NOTE:** If on Linux you experience troubles with installing `PyQt5`,
try running this command:

```bash
sudo apt update && sudo apt upgrade
sudo apt install python3-pyqt5
```

And edit the `.venv/pyvenv.cfg` line `include-system-site-packages` from `false`
to `true`

Build an executable (make sure your venv is activated)

- macOs/Linux:

```bash
sh build.sh
```

- Windows:

```bash
.\build.ps1
```

Executable will be located in `dist/` directory and you can launch it from here.
Otherwise, download pre-built executable from [Releases](https://github.com/kvmvkxnt/csit040_final_project/releases/latest).

Using Github Releases.

- macOs:
  Download macOs release for your system, unzip and launch the .app.
- Windows:
  Download Windows release for your system, unzip and just run the executable.
- Linux:
  Who creates binaries for linux? Be a man, build yourself from source or just use
  python.
