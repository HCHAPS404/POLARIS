/*
 * POLARIS field node firmware stub — target: STM32 NUCLEO N657X0-Q (DESIGNED).
 * Evidence: PLACEHOLDER (state machine contract only; not flashed in CI).
 */

#include "node.h"

void node_init(node_context_t *ctx)
{
    if (ctx == 0) {
        return;
    }
    ctx->state = NODE_BOOT;
    ctx->sample_count = 0;
    ctx->tx_count = 0;
}

node_state_t node_tick(node_context_t *ctx)
{
    if (ctx == 0) {
        return NODE_BOOT;
    }

    switch (ctx->state) {
    case NODE_BOOT:
        ctx->state = NODE_SAMPLE;
        break;
    case NODE_SAMPLE:
        ctx->sample_count += 1;
        /* ADC / I2C pluviometer or level driver — see configs/devices/ */
        ctx->state = NODE_TRANSMIT;
        break;
    case NODE_TRANSMIT:
        ctx->tx_count += 1;
        /* LoRa sub-GHz TX — packet built to simulation.python.iot.comm contract */
        ctx->state = NODE_SLEEP;
        break;
    case NODE_SLEEP:
        ctx->state = NODE_SAMPLE;
        break;
    }
    return ctx->state;
}

#ifdef POLARIS_NODE_HOST_TEST
int main(void)
{
    node_context_t ctx;
    node_init(&ctx);
    for (int i = 0; i < 8; i++) {
        node_tick(&ctx);
    }
    return (int)ctx.tx_count;
}
#endif
