# workq

workq is a simple distributed work queue for CPU-bound batch jobs, built with Redis and Docker.

The system consists of a job producer, a Redis-backed queue, and multiple worker containers.
Jobs reference input artifacts stored on shared disk and are processed independently by workers.
The project focuses on throughput, scheduling behavior, and operational simplicity.

## Motivation

This project explores the design and implementation of a simple distributed work queue.
The goal is to understand how jobs are scheduled, dispatched, and executed across multiple workers
under constrained CPU resources, and how throughput scales with additional workers.

## System Overview

workq is composed of three primary components:

- **Producer**: Enqueues jobs into Redis.
- **Queue**: A Redis-backed work queue that coordinates job dispatch.
- **Workers**: Stateless worker processes that claim and execute jobs.

Input and output artifacts are stored on shared disk volumes mounted into the producer
and worker containers.

## Architecture

The system is deployed using Docker Compose and consists of the following containers:

- `producer`
- `redis`
- `worker` (replicated)

Workers pull jobs from Redis, process them, and write results to shared storage.

## Job Model

Each job represents a single image transformation task:

- Read an input image from shared storage
- Resize the image
- Convert it to grayscale
- Write the output image to shared storage

Jobs are independent and idempotent.

## Queue Semantics

Jobs are enqueued in Redis and claimed by workers using atomic operations.
Once a worker claims a job, it is responsible for executing it and marking it complete.

The queue is designed to ensure:
- At-most-once execution
- No coordination between workers
- Simple failure behavior

## Throughput & Metrics

The producer records timestamps when jobs are enqueued.
Workers record timestamps when jobs begin and complete execution.

These metrics are used to measure:
- Enqueue rate
- Execution rate
- End-to-end throughput

## Running the System

```bash
docker-compose up --build

## Limitations & Future Work

- No job retry or failure recovery
- No priority scheduling
- Redis is a single point of failure
- CPU-only execution

Future improvements may include job retries, backpressure handling, and alternative queue backends.

## Design Philosophy

The system favors simplicity and explicit control flow over abstraction.
Most components are implemented as small, focused functions with minimal shared state.

## License

MIT
