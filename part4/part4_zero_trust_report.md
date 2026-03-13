# Part 4 - Secure Distributed Communication Report

Date: 2026-03-13

## Goal

- Apply zero-trust principles to inter-service communication.

## Problem Addressed

- File service previously trusted request parameters directly.
- Any caller could claim user identity without strong proof.

## Controls Implemented

- Auth service issues signed short-lived access tokens.
- File service requires token (`X-Access-Token` header or `token` query).
- Auth and file services must share the same `INTER_SERVICE_SECRET` value.
- File service verifies:
  - token format
  - HMAC signature
  - expiration time
  - user/role claim consistency
  - request user matches token user

## Validation Performed

1. Missing token denied

- Script: [part4/missing_token_denied_test.py](part4/missing_token_denied_test.py)
- Expected: `401`.

2. Valid token allows authorized access

- Script: [part4/valid_token_allows_access_test.py](part4/valid_token_allows_access_test.py)
- Expected: `200` encrypted response.

3. Identity mismatch denied

- Script: [part4/identity_mismatch_denied_test.py](part4/identity_mismatch_denied_test.py)
- Expected: `403`.

4. Tampered token denied

- Script: [part4/tampered_token_denied_test.py](part4/tampered_token_denied_test.py)
- Expected: `401` invalid signature.

## Security Outcome

- File service no longer trusts unauthenticated caller claims.
- Access decisions now depend on signed token claims and RBAC policy.

## Residual Risk

- Replay protection is still needed (observed in Part 5).
- A valid token can be reused within its validity window unless anti-replay controls are added.
