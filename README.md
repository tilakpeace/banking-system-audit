# banking-system-audit
This MVP project demonstrates basic simulated banking operations. Instead of using a database, account data is temporarily stored in an in-memory structure called accounts_snapshot. In a real production environment, this should be replaced with a proper database implementation. Additionally, all activity logs are maintained in memory under events. The primary goal of this project is to showcase replay functionality for data reconstruction.



## Project Setup

Command for project setup 

* python -m venv venv 
* source venv/bin/activate
* pip install -r requirements.txt
* python app.py 
* Access url : http://127.0.0.1:5000/



## Overview

This document provides information on the available API endpoints, including their purpose, request formats, and response structures.

---

## Base URL

```
http://127.0.0.1:5000
```

---

## Endpoints

### 1. **Open Account**

**POST** `/accounts/open`

#### **Request Body (JSON)**

```json
{
  "customer_name": "Alex Smith"
}
```

#### **Response**

```json
{
    "account_id": "2db734d1",
    "balance": 0.0,
    "message": "Account opened successfully"
}
```

---

### 2. **Deposit**

**POST** `accounts/<account_id>/deposit`

#### **Request Body (JSON)**

```json
{

    "amount":2003,
    "description":"this is deposit testing"
}
```

#### **Response**

```json
{
    "account_id": "f8c8a0a8",
    "amount": 2003.0,
    "message": "Deposit successful",
    "new_balance": 6009.0
}
```

---

### 3. **Withdraw**

**POST** `accounts/<account_id>/withdraw`

#### **Request Body (JSON)**

```json
{

    "amount":33,
    "description":"this is withdraw testing"
}
```


#### **Response**

```json
{
    "account_id": "f8c8a0a8",
    "amount": 33.0,
    "message": "Withdrawal successful",
    "new_balance": 5910.0
}
```

---

### 4. **Transfer**

**POST** `accounts/<account_id>/transfer`

#### **Request Body (JSON)**

```json
{

    "to_account_id":"2db734d1",
    "amount":"500"
}
```

#### **Response**

```json
{
    "amount": 500.0,
    "from_account_balance": 1503.0,
    "message": "Transfer successful",
    "to_account_balance": 500.0,
    "transfer_id": "0b01d71a-a776-4aa5-b009-42545728c50a"
}
```

---

### 5. **Close**

**POST** `/accounts/<account_id>/close`

#### **Request Body (JSON)**

```json
{
    "reason":"close account test"
}
```

#### **Response**

```json
{
    "account_id": "33484e9c",
    "final_balance": 0.0,
    "message": "Account closed successfully"
}
```

---

### 6. **Account Detail**

**GET** `/accounts/<account_id>`

#### **Response**

```json
{
    "account_id": "be69e28b",
    "balance": 500.0,
    "created_at": "2025-11-22T00:43:29.772345",
    "customer_name": "Test User",
    "status": "active",
    "transaction_count": 1,
    "transactions": [
        {
            "amount": 500.0,
            "balance_after": 500.0,
            "description": "Transfer from 55c5c617",
            "timestamp": "Sat, 22 Nov 2025 00:43:36 GMT",
            "type": "deposit"
        }
    ]
}
```

---



### 7. **All Accounts Detail**

**GET** `/accounts`

#### **Response**

```json
{
    "accounts": {
        "2db734d1": {
            "account_id": "2db734d1",
            "balance": 500.0,
            "created_at": "2025-11-22T00:11:05.701108",
            "customer_name": "Test User",
            "status": "active",
            "transaction_count": 1,
            "transactions": [
                {
                    "amount": 500.0,
                    "balance_after": 500.0,
                    "description": "Transfer from f8c8a0a8",
                    "timestamp": "Sat, 22 Nov 2025 00:11:15 GMT",
                    "type": "deposit"
                }
            ]
        },
        "33484e9c": {
            "account_id": "33484e9c",
            "balance": 0.0,
            "created_at": "2025-11-22T00:08:51.767542",
            "customer_name": "Test User",
            "status": "closed",
            "transaction_count": 0,
            "transactions": []
        },
        "f8c8a0a8": {
            "account_id": "f8c8a0a8",
            "balance": 5410.0,
            "created_at": "2025-11-22T00:10:25.303593",
            "customer_name": "Test User",
            "status": "active",
            "transaction_count": 7,
            "transactions": [
                {
                    "amount": 2003.0,
                    "balance_after": 2003.0,
                    "description": "this is deposit testing",
                    "timestamp": "Sat, 22 Nov 2025 00:10:35 GMT",
                    "type": "deposit"
                },
                {
                    "amount": 2003.0,
                    "balance_after": 4006.0,
                    "description": "this is deposit testing",
                    "timestamp": "Sat, 22 Nov 2025 00:10:36 GMT",
                    "type": "deposit"
                },
                {
                    "amount": 2003.0,
                    "balance_after": 6009.0,
                    "description": "this is deposit testing",
                    "timestamp": "Sat, 22 Nov 2025 00:10:40 GMT",
                    "type": "deposit"
                },
                {
                    "amount": 33.0,
                    "balance_after": 5976.0,
                    "description": "this is withdraw testing",
                    "timestamp": "Sat, 22 Nov 2025 00:10:47 GMT",
                    "type": "withdrawal"
                },
                {
                    "amount": 33.0,
                    "balance_after": 5943.0,
                    "description": "this is withdraw testing",
                    "timestamp": "Sat, 22 Nov 2025 00:10:47 GMT",
                    "type": "withdrawal"
                },
                {
                    "amount": 33.0,
                    "balance_after": 5910.0,
                    "description": "this is withdraw testing",
                    "timestamp": "Sat, 22 Nov 2025 00:10:54 GMT",
                    "type": "withdrawal"
                },
                {
                    "amount": 500.0,
                    "balance_after": 5410.0,
                    "description": "Transfer to 2db734d1",
                    "timestamp": "Sat, 22 Nov 2025 00:11:15 GMT",
                    "type": "withdrawal"
                }
            ]
        }
    },
    "total_accounts": 3
}
```

---

### 8. **Get all Events**

**GET** `/events`

#### **Response**

```json
{
    "events": [
        {
            "account_id": "33484e9c",
            "data": {
                "customer_name": "Test User",
                "initial_balance": 0.0
            },
            "event_id": "1b8f23a3-6207-4791-8844-ab25ede827be",
            "event_type": "account_opened",
            "timestamp": "2025-11-22T00:08:51.767486"
        },
        {
            "account_id": "33484e9c",
            "data": {
                "final_balance": 0.0,
                "reason": "close account test"
            },
            "event_id": "50672985-9996-4351-b3ef-e10cf26ad924",
            "event_type": "account_closed",
            "timestamp": "2025-11-22T00:10:07.428003"
        },
        {
            "account_id": "f8c8a0a8",
            "data": {
                "customer_name": "Test User",
                "initial_balance": 0.0
            },
            "event_id": "5b12dd85-9cac-4583-b404-237d538e24fa",
            "event_type": "account_opened",
            "timestamp": "2025-11-22T00:10:25.303566"
        },
        {
            "account_id": "f8c8a0a8",
            "data": {
                "amount": 2003.0,
                "description": "this is deposit testing"
            },
            "event_id": "61172898-060d-4fc1-8b82-78d73e71ec4c",
            "event_type": "funds_deposited",
            "timestamp": "2025-11-22T00:10:35.763571"
        },
        {
            "account_id": "f8c8a0a8",
            "data": {
                "amount": 2003.0,
                "description": "this is deposit testing"
            },
            "event_id": "a2002d65-62ad-4fe9-88a3-f528a21e493f",
            "event_type": "funds_deposited",
            "timestamp": "2025-11-22T00:10:36.346944"
        },
        {
            "account_id": "f8c8a0a8",
            "data": {
                "amount": 2003.0,
                "description": "this is deposit testing"
            },
            "event_id": "3c6708d6-6ef7-497f-a19d-c38f326bf7e6",
            "event_type": "funds_deposited",
            "timestamp": "2025-11-22T00:10:40.312741"
        },
        {
            "account_id": "f8c8a0a8",
            "data": {
                "amount": 33.0,
                "description": "this is withdraw testing"
            },
            "event_id": "f4adbd4d-8535-4ba8-8248-eeea2a083aa1",
            "event_type": "funds_withdrawn",
            "timestamp": "2025-11-22T00:10:47.130705"
        },
        {
            "account_id": "f8c8a0a8",
            "data": {
                "amount": 33.0,
                "description": "this is withdraw testing"
            },
            "event_id": "d9b2d9b1-728c-407d-aeab-dcda32da32f2",
            "event_type": "funds_withdrawn",
            "timestamp": "2025-11-22T00:10:47.964054"
        },
        {
            "account_id": "f8c8a0a8",
            "data": {
                "amount": 33.0,
                "description": "this is withdraw testing"
            },
            "event_id": "bd537429-660e-4cad-add8-95e22b711d27",
            "event_type": "funds_withdrawn",
            "timestamp": "2025-11-22T00:10:54.404882"
        },
        {
            "account_id": "2db734d1",
            "data": {
                "customer_name": "Test User",
                "initial_balance": 0.0
            },
            "event_id": "ea392477-5f0c-417c-b8df-8ef158ddbe68",
            "event_type": "account_opened",
            "timestamp": "2025-11-22T00:11:05.701078"
        },
        {
            "account_id": "f8c8a0a8",
            "data": {
                "amount": 500.0,
                "description": "Transfer to 2db734d1",
                "transfer_id": "3d832218-462d-4118-a173-db403b411bcc"
            },
            "event_id": "a28d928d-7fec-4955-be16-cd301fa54187",
            "event_type": "funds_withdrawn",
            "timestamp": "2025-11-22T00:11:15.565982"
        },
        {
            "account_id": "2db734d1",
            "data": {
                "amount": 500.0,
                "description": "Transfer from f8c8a0a8",
                "transfer_id": "3d832218-462d-4118-a173-db403b411bcc"
            },
            "event_id": "1afa7dd4-7633-4549-af16-623a48bcbd99",
            "event_type": "funds_deposited",
            "timestamp": "2025-11-22T00:11:15.566016"
        }
    ],
    "total_events": 12
}
```

---


### 9. **Replay**

**POST** `/replay`

#### **Request Body (JSON)**

```json
{
}
```

#### **Response**

```json
{
    "accounts_after": 3,
    "accounts_before": 3,
    "accounts_rebuilt": 3,
    "events_checksum": "4b5eccb4baccd194abdbe061a334a520e07d0a3ea760d6d552444022c86c5e40",
    "events_processed": 12,
    "message": "Event replay completed successfully",
    "state_checksum": "eae94d7c32a0deeb9dc646fb655a80a0620810055917e0a6bb451f83a47f1c9a",
    "verification": "Identical checksums across replays confirm determinism"
}
```

---
