                       +---------------------+
                       |   Client (User/IP)  |
                       +---------+-----------+
                                 |
                                 ▼
                    +--------------------------+
                    | FastAPI App (main.py)    |
                    | - Endpoint Handler       |
                    | - Middleware Layer       |
                    +-----------+--------------+
                                |
                                ▼
           +----------------------------------------+
           | Rate Limiter (limiter.py)              |
           | - Token Bucket or Sliding Window       |
           | - Tracks per IP/API key                |
           +----------------+-----------------------+
                            |
                            ▼
                     +-----------+
                     | Redis     |  ◄────── Abuse Score, Counters
                     +-----------+
                            ▲
                            |
        +------------------------------------------+
        | Abuse Detection Engine (abuse_detection.py) |
        | - Rule-based heuristics                   |
        | - Tracks patterns and assigns scores      |
        +------------------------------------------+

Optional:
                            ▼
                 +--------------------+
                 | Analytics DB (e.g.,|
                 | PostgreSQL or log) |
                 +--------------------+

