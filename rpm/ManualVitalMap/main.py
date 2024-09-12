import random
import time

def get_tokens():
    tokens = [
        '0oR3jpoG4js7nAeTRmWaHWVaSqcZK8wL-tohnghfDCc',
        "OkHDro_lR1Gnu6Mi001hIa8phXKZ5375JwdLRwwc64w",
        "ftnsNf-oJX-527gkravKR8lMlIIJVTteZMfuICbjYUA"
    ]
    
    return tokens

def main():
    import manualbloodglucose
    import manualbloodoxygen
    import manualbloodpressure
    import manualheartrate
    import manualtempeture
    # import manualheight
    import manualweight
    
    tokens = get_tokens()

    for i in range(30):
        for bearer_token in tokens:
            manualbloodglucose.manualglucose(bearer_token)
            manualbloodoxygen.manualoxygen(bearer_token)
            manualbloodpressure.manualbloodpressure(bearer_token)
            manualheartrate.manualheartrate(bearer_token)
            manualtempeture.manualtemp(bearer_token)
            # manualheight.manualheight(bearer_token)
            manualweight.manualweight(bearer_token)
            print(f"{i}--Manual Data seeded successfully with token {bearer_token} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Sleep for 5 minutes
        time.sleep(180)

if __name__ == "__main__":
    main()
