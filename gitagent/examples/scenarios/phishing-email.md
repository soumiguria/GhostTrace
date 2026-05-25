# Scenario: Microsoft phishing email

## Input

```
URGENT: Your Microsoft account will be suspended in 24 hours.
Verify immediately: https://micros0ft-security-verify.net/login
Contact: support@micros0ft-security-verify.net
```

## Expected

- Entities: typosquatted domain, suspicious URL, support email
- Red flags: urgency, account verification pattern
- Risk: elevated (50+)
- Classification: Likely phishing attempt
