# PulseMQ

## TODO

- [ ] Create class Broker
- [ ] Create class Consumer
- [ ] Performantly handle multiple concurrent client connections
- [ ] Statistics with export methods to Prometheus or ClickHouse
- [ ] Track for growing errors to specific Consumers, if we see a sharp spike, temporarily pause consuming to this to help reduce backpressure

- [ ] Create class MessageQueue
- [ ] Create class Message
- [ ] Track ACKs per consumer
- [ ] Config parameters per MessageQueue (max ACKs, duration between ACKs, how often to check)
- [ ] Persistence (to disk) for durable queues
- [ ] Dead Letter Queue, check after 1/2 minutes if Consumer has pinged recently enough to receive the message again, if fail, don't retry, leave in DLQ. DLQ will dump to disk, never stay in men. Will also read from disk. Max per DLQ configurable as a global but not per MessageQueue

- [ ] Create class ClientConnection (parses commands and routes to Broker)
- [ ] Create async TCP server and link with ClientConnection
- [ ] Implement client command parsing and handling (`PUBLISH` for adding messages to queue, `CONSUME` with modes burst/round robin, `ACK` to not resend anymore, `PING`, `DISCONNECT`, `CREATE_QUEUE`)

- [ ] Graceful shutdown (e.g clear all messages, refuse new ones, disconnect clients and tell them to reconnect in X delay)
- [ ] Extensive unit and integration tests
- [ ] Error handing and client disconnect logic
- [ ] Extensive logging + configurable verbosity (debug/info/warning/error)
- [ ] Create client sided module for publishing/consuming etc
- [ ] README.md for overall project including screenshots
- [ ] Docs/examples etc
