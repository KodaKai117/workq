# workq

A distributed job queue for batch image processing, built with Redis and Python.

## Project Status

**Currently Working (v0.1):**
-  Producer scans input directory and enqueues jobs to Redis
-  Worker polls Redis queue and processes jobs
-  Basic image transformation (resize to 256x256, grayscale conversion)
-  JSON-based configuration

**In Progress:**
- Error handling and recovery
- Structured logging
- Job completion tracking

**Planned (v0.2+):**
- Docker containerization
- Multi-worker deployment
- Performance metrics and monitoring
- Graceful shutdown handling

## Current Architecture
```
input/          →  [Producer]  →  [Redis Queue]  →  [Worker]  →  output/
(raw images)       (enqueue)       (jobs list)       (process)     (processed)
```

## Quick Start

1. Install dependencies: `pip install redis pillow`
2. Start Redis: `redis-server`
3. Configure paths in `interface/config/transform.json`
4. Run producer: `python producer/producer.py`
5. Run worker: `python worker/worker.py`

## Future Work

- Docker Compose deployment
- Horizontal worker scaling  
- Job retry and dead letter queues
- Throughput analysis and benchmarking

## License

MIT