/*
 * POLARIS field node — state machine contract (DESIGNED / PLACEHOLDER).
 * Target: STM32 NUCLEO N657X0-Q. Not flashed in CI.
 */
#ifndef POLARIS_NODE_H
#define POLARIS_NODE_H

typedef enum {
    NODE_BOOT = 0,
    NODE_SAMPLE,
    NODE_TRANSMIT,
    NODE_SLEEP,
} node_state_t;

typedef struct {
    node_state_t state;
    unsigned sample_count;
    unsigned tx_count;
} node_context_t;

void node_init(node_context_t *ctx);
node_state_t node_tick(node_context_t *ctx);

#endif
