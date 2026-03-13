# Part 5 - Attack Testing Report

Date: 2026-03-13

## Scope

- Attempt to bypass access control
- Attempt token replay
- Attempt restricted file access

## Execution Summary

- Run scripts from [part5/part5.py](part5/part5.py)
- Mark each test as BLOCKED or VULNERABLE based on output

## Findings

### Access Control Bypass

- Status: BLOCKED
- Evidence: [part5/bypass_access_control_test.py](part5/bypass_access_control_test.py) returned status 403 with response {"error":"Access denied","requiredRole":"manager"} when staff tried manager file.

### Restricted File Access

- Status: BLOCKED
- Evidence: [part5/access_restricted_files_test.py](part5/access_restricted_files_test.py) returned status 401 without token and 403 for user identity mismatch.

### Replay Token

- Status: BLOCKED
- Evidence: [part5/replay_token_test.py](part5/replay_token_test.py) now returns status 200 on first use and 401 with `{"error":"Replay token detected"}` on replay.

## Notes

- If replay token attempt returns 200 on both first and second use, replay protection is missing.
- Anti-replay control implemented: one-time token use based on token `jti` tracking in file service.
