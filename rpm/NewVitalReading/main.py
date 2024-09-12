import time

def get_tokens():
    return [
        '0oR3jpoG4js7nAeTRmWaHWVaSqcZK8wL-tohnghfDCc',
        "OkHDro_lR1Gnu6Mi001hIa8phXKZ5375JwdLRwwc64w",
        "ftnsNf-oJX-527gkravKR8lMlIIJVTteZMfuICbjYUA"
        
    ]

def main():
    import accucheck
    import tngspo2
    import weight
    import tempeture
    import testngo

    tokens = get_tokens()
    
    for i in range(20):
        for bearer_token in tokens:
            accucheck.accucheck(bearer_token)
            tngspo2.tngspo2(bearer_token)
            weight.weight(bearer_token)
            tempeture.temp(bearer_token)
            testngo.testngo(bearer_token)
            print(f"{i}--Data seeded successfully with token {bearer_token} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Sleep for 3 minutes before the
        time.sleep(180)

if __name__ == "__main__":
    main()