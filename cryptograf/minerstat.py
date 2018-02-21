from scrapeDstmStats import writeGpuStatsToInflux
from wtmApiPoll import writeWtmFeedToInflux

def main():

    writeGpuStatsToInflux()

    writeWtmFeedToInflux()

if __name__ == "__main__":
    main()