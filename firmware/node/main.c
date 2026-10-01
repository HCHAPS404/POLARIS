/*
 * POLARIS field node firmware stub — target: STM32 NUCLEO N657X0-Q (DESIGNED).
 * Evidence: PLACEHOLDER (state machine contract only; not flashed in CI).
 *
 * States: BOOT → SAMPLE → TRANSMIT → SLEEP (SELF_TEST/FILTER omitted in stub).
 */

typedef enum {
    NODE_BOOT = 0,
    NODE_SAMPLE,
    NODE_TRANSMIT,
    NODE_SLEEP,
} node_state_t;

static node_state_t state = NODE_BOOT;

void node_tick(void)
{
    switch (state) {
    case NODE_BOOT:
        state = NODE_SAMPLE;
        break;
    case NODE_SAMPLE:
        /* ADC / I2C pluviometer or level driver — see configs/devices/ */
        state = NODE_TRANSMIT;
        break;
    case NODE_TRANSMIT:
        /* LoRa sub-GHz TX — packet built to simulation.python.iot.comm contract */
        state = NODE_SLEEP;
        break;
    case NODE_SLEEP:
        /* Low-power wait for sample_interval_s */
        state = NODE_SAMPLE;
        break;
    }
}
