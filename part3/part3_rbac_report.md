# Part 3 - RBAC Implementation Report

Date: 2026-03-13

## Goal

- Enforce role-based access control on file requests.

## Policy Implemented

User roles:

- `adminCed` -> `manager`
- `employeeStyl` -> `staff`

File access policy:

- `salary.xlsx` -> `manager`
- `meetingNotes.txt` -> `staff`

## Validation Performed

1. Login role verification

- Script: [part3/login_role_test.py](part3/login_role_test.py)
- Expected: login returns role data.

2. Manager access to salary file

- Script: [part3/manager_salary_access_test.py](part3/manager_salary_access_test.py)
- Expected: status `200` and encrypted response.

3. Staff denied salary file

- Script: [part3/staff_salary_denied_test.py](part3/staff_salary_denied_test.py)
- Expected: status `403` with access denied.

4. Staff access to meeting notes

- Script: [part3/staff_meeting_access_test.py](part3/staff_meeting_access_test.py)
- Expected: status `200` and encrypted response.

5. Missing user check

- Script: [part3/missing_user_denied_test.py](part3/missing_user_denied_test.py)
- Expected: with a valid token, request still succeeds because identity is derived from token claims.

## Security Outcome

- Direct access by filename is no longer sufficient.
- Role checks now gate access to protected files.
- In the current architecture, token claims are the identity source of truth for RBAC checks.

## Residual Risk

- Role claims must come from a trusted source.
- Inter-service trust and token integrity are handled in Part 4.
