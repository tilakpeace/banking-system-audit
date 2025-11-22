
import requests

BASE_URL = "http://127.0.0.1:5000"

def main():
    print("Testing Bank Operations & Replay Determinism...")
    
    # 1. Open accounts
    print("\n1. Opening accounts...")
    acc1 = requests.post(f"{BASE_URL}/accounts/open", json={
        "customer_name": "John Doe"
    }).json()
    acc1_id = acc1["account_id"]
    print(f"   Account 1: {acc1_id}, Balance: ${acc1['balance']}")
    
    acc2 = requests.post(f"{BASE_URL}/accounts/open", json={
        "customer_name": "Jane Smith"
    }).json()
    acc2_id = acc2["account_id"]
    print(f"   Account 2: {acc2_id}, Balance: ${acc2['balance']}")
    
    # 2. Deposit
    print("\n2. Making deposit...")
    deposit = requests.post(f"{BASE_URL}/accounts/{acc1_id}/deposit", json={
        "amount": 800
    }).json()
    print(f"   Deposited ${300} to {acc1_id}, New balance: ${deposit['new_balance']}")
    
    # 3. Withdraw
    print("\n3. Making withdrawal...")
    withdraw = requests.post(f"{BASE_URL}/accounts/{acc1_id}/withdraw", json={
        "amount": 200
    }).json()
    print(f"   Withdrew ${200} from {acc1_id}, New balance: ${withdraw['new_balance']}")
    
    # 4. Transfer
    print("\n4. Making transfer...")
    transfer = requests.post(f"{BASE_URL}/accounts/{acc1_id}/transfer", json={
        "to_account_id": acc2_id,
        "amount": 150
    }).json()
    print(f"   Transferred ${150} from {acc1_id} to {acc2_id}")
    print(f"   {acc1_id} balance: ${transfer['from_account_balance']}")
    print(f"   {acc2_id} balance: ${transfer['to_account_balance']}")
    
    # 5. Close account
    print("\n5. Closing account...")
    close = requests.post(f"{BASE_URL}/accounts/{acc2_id}/close", json={
        "reason": "Test completion"
    }).json()
    print(f"   Closed account {acc2_id}, Final balance: ${close['final_balance']}")
    
    # 6. Test replay determinism
    print("\n6. Testing replay determinism...")
    
    # First replay
    r1 = requests.post(f"{BASE_URL}/replay")
    result1 = r1.json()
    checksum1 = result1["state_checksum"]
    print(f"   First replay:  {checksum1[:20]}...")
    
    # Second replay  
    r2 = requests.post(f"{BASE_URL}/replay")
    result2 = r2.json()
    checksum2 = result2["state_checksum"]
    print(f"   Second replay: {checksum2[:20]}...")
    
    # Third replay
    r3 = requests.post(f"{BASE_URL}/replay")
    result3 = r3.json()
    checksum3 = result3["state_checksum"]
    print(f"   Third replay:  {checksum3[:20]}...")
    
    # Verify all checksums are identical
    assert checksum1 == checksum2 == checksum3, \
        "All replays should produce identical checksums"
    
    print("\n✅ All operations completed successfully!")
    print("✅ Replay system is deterministic!")
    print(f"✅ Final checksum: {checksum1[:32]}...")

if __name__ == "__main__":
    main()