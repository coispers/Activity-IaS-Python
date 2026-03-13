# Activity-IaS-Python

Security hardening lab project with 5 progressive parts:

- Part 1: Reconnaissance and exploitation baseline checks
- Part 2: Encryption of sensitive file responses
- Part 3: Role-Based Access Control (RBAC)
- Part 4: Zero-trust inter-service token validation
- Part 5: Attack testing (including replay attack verification)

## Project Structure

- auth_server.py
- file_server.py
- part1/
- part2/
- part3/
- part4/
- part5/

Each part folder contains:

- a runner script (partX.py)
- test scripts for that part
- a report markdown file

## Prerequisites

- Python 3.13+
- Windows PowerShell (examples below use PowerShell)

## Setup

1. Open a terminal in the project root:

```powershell
cd "d:\Activity IaS Python"
```

2. Activate your virtual environment:

```powershell
& ".venv\Scripts\Activate.ps1"
```

3. Install dependencies (if not installed yet):

```powershell
pip install flask cryptography
```

## Start the Servers

Open two separate terminals in project root and run:

Terminal A (Auth Server):

```powershell
$env:INTER_SERVICE_SECRET="part4-shared-secret"
python auth_server.py
```

Terminal B (File Server):

```powershell
$env:INTER_SERVICE_SECRET="part4-shared-secret"
python file_server.py
```

Important:

- Both servers must use the same INTER_SERVICE_SECRET.
- Keep both terminals running while executing part scripts.

## Run Part Scripts (1 to 5)

Open a third terminal in project root and run one part at a time.

### Part 1

```powershell
python part1/part1.py
```

### Part 2

```powershell
python part2/part2.py
```

### Part 3

```powershell
python part3/part3.py
```

### Part 4

```powershell
python part4/part4.py
```

### Part 5

```powershell
python part5/part5.py
```

Notes:

- Each runner prompts: Press Enter to continue to ...
- Type q to stop a part runner.
- Runners continue to the next test even if one test fails.
